package com.shivamjha2712.LearningRESTAPIs.advices;

import org.springframework.core.MethodParameter;
import org.springframework.http.MediaType;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseBodyAdvice;

/**
 * GlobalResponseHandler:
 * Yeh class har controller se return hone wale response ko intercept karne ke liye hai.
 * Tum yahan response ko modify / wrap / log / transform kar sakte ho before woh client ko mile.
 * <p>
 * Note:
 * - Agar supports() true return karta hai to beforeBodyWrite() har response pe chalega.
 * - Agar beforeBodyWrite() null return karega to original response body replace ho jayega -> usually galat.
 * - Is file me minimal safe behavior: original body ko hi wapas bhejenge (no-op), saath me comments diye hue hain
 * ki agar tum wrapper/format change karna chaho to kaise kar sakte ho.
 */
@RestControllerAdvice
public class GlobalResponseHandler implements ResponseBodyAdvice<Object> {

    /**
     * supports(...)
     * - Spring ko batata hai ki kya ye advice kisi particular controller/method ke response par apply hona chahiye.
     * - current implementation "return true" hai, matlab sabhi responses pe apply hoga.
     * <p>
     * Agar tum kuch responses skip karna chahte ho (jaise file download, byte[] stream, ya already wrapped responses),
     * to yahan conditional laga sakte ho, for example:
     * <p>
     * // pseudo
     * if (returnType.getParameterType() == MyWrapper.class) return false;
     * <p>
     * Isse infinite wrapping aur incompatible media type issues avoid hote hain.
     */
    @Override
    public boolean supports(MethodParameter returnType, Class<? extends HttpMessageConverter<?>> converterType) {
        // Simple/Default: advice sab responses par chalega
        return true;
    }

    /**
     * beforeBodyWrite(...)
     * - Yeh method controller ka jo "body" return hua hai use bhejne se pehle call hota hai.
     * - body argument me controller se return hua asli object aata hai (DTO, List, Map, String, etc).
     * <p>
     * IMPORTANT:
     * - Agar yahan `return null;` kar doge toh client ko null/empty response milega aur bohot bugs aate hain.
     * - Minimal safe behavior: original body ko wapas return karo -> `return body;`
     * <p>
     * Common use-cases:
     * 1) Pass-through (no change) -> return body;
     * 2) Standard wrapper -> return a Map/DTO like { status, message, data: body }
     * 3) Conditional wrapping -> skip for certain media types (e.g., byte[]), or for error responses
     * <p>
     * Example of wrapper (optional, commented):
     * Map<String,Object> envelope = new HashMap<>();
     * envelope.put("status", 200);
     * envelope.put("message", "success");
     * envelope.put("data", body);
     * return envelope;
     * <p>
     * Important skip rules when wrapping:
     * - Do NOT wrap types like byte[] (file downloads) or ResponseEntity already carrying status/headers.
     * - Do NOT wrap ApiError or exception payloads (handle them via exception handler).
     * <p>
     * Current implementation returns the original body (safe default).
     */
    @Override
    public Object beforeBodyWrite(Object body,
                                  MethodParameter returnType,
                                  MediaType selectedContentType,
                                  Class<? extends HttpMessageConverter<?>> selectedConverterType,
                                  ServerHttpRequest request,
                                  ServerHttpResponse response) {

        // If you want to debug/log every response, you can log here:
        // System.out.println("GlobalResponseHandler - response body type: " + (body != null ? body.getClass() : "null"));

        // SAFEST DEFAULT: original body ko wapas bhej do (no-op)
        // Agar tum isko replace karoge to ensure non-null aur compatible type ho.
        if (body instanceof ApiResponse) {
            return body;
        } else {
            return new ApiResponse(body);
        }

        // -------------------------
        // Example: agar tum uniform wrapper chahte ho, use kar sakte ho (uncomment and adapt):
        //
        // if (body == null) {
        //     Map<String, Object> envelope = new HashMap<>();
        //     envelope.put("status", 204);
        //     envelope.put("message", "No Content");
        //     envelope.put("data", null);
        //     return envelope;
        // }
        //
        // // don't wrap already wrapped responses or error objects
        // if (body instanceof ApiError || body instanceof MyWrapperType) {
        //     return body;
        // }
        //
        // Map<String, Object> envelope = new HashMap<>();
        // envelope.put("status", 200);
        // envelope.put("message", "success");
        // envelope.put("data", body);
        // return envelope;
    }
}