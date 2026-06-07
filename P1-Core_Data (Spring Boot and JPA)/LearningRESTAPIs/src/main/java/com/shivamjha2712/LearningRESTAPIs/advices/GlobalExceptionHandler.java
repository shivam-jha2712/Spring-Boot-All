package com.shivamjha2712.LearningRESTAPIs.advices;

import com.shivamjha2712.LearningRESTAPIs.exceptions.ResourceNotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.List;
import java.util.stream.Collectors;

/**
 * GlobalExceptionHandler
 * <p>
 * Hinglish summary:
 * - Yeh class application-wide exceptions ko centralize karke handle karti hai.
 * - Controller se jab koi exception throw hota hai, Spring yahan corresponding @ExceptionHandler
 * method ko call karega aur hum standardized `ApiResponse<ApiError>` bhejenge.
 * - Standard format se client-side pe error handling consistent ho jaati hai.
 * <p>
 * Note:
 * - Success responses ko tumhara `GlobalResponseHandler` wrap karta hai (ApiResponse).
 * - Error responses yahan ApiError create karke `ApiResponse<ApiError>` me bheje jaate hain.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * handleResourceNotFound
     * <p>
     * Hinglish:
     * - Ye handler `ResourceNotFoundException` ko catch karta hai (jab koi requested resource na mile).
     * - Hum ek `ApiError` banate hain jisme HTTP 404 status aur descriptive message hota hai.
     * - Fir `buildErrorResponseEntity` ko use karke `ApiResponse<ApiError>` ke saath response bhejte hain.
     * <p>
     * Behavior:
     * - Client ko HTTP 404 status milega aur body me `ApiResponse` jisme `error` field set hogi.
     */
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiResponse<?>> handleResourceNotFound(ResourceNotFoundException exception) {
        ApiError apiError = ApiError.builder()
                .status(HttpStatus.NOT_FOUND)
                .message(exception.getMessage())
                .build();
        return buildErrorResponseEntity(apiError);
    }

    /**
     * handleInternalServerError
     * <p>
     * Hinglish:
     * - Generic fallback handler for any uncaught `Exception`.
     * - Production me aise generic handler important hai taaki server-side stack traces client pe na jayein.
     * - Yahan hum HTTP 500 aur exception message ko `ApiError` me wrap kar ke bhejte hain.
     * <p>
     * Behavior:
     * - Client ko HTTP 500 aur standardized `ApiResponse<ApiError>` milega.
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse<?>> handleInternalServerError(Exception exception) {
        ApiError apiError = ApiError.builder()
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .message(exception.getMessage())
                .build();
        return buildErrorResponseEntity(apiError);
    }

    // Example note (Hinglish):
    // - Neeche waala MethodArgumentNotValidException handler validation errors ko readable list me convert karta hai.
    // - Ye default bindResult messages ko collect karke client ko bhejta hai in `subErrors` field ke through.

    /**
     * handleMethodArgumentNotValid
     * <p>
     * Hinglish:
     * - Jab controller method ke @Valid annotated parameters fail karte hain, Spring `MethodArgumentNotValidException` throw karta hai.
     * - Hum bindingResult se saare error messages collect kar ke `subErrors` list banate hain.
     * - Fir ApiError me status 400 aur message "Input Validation Failed" ke saath bhejte hain.
     * <p>
     * Behavior:
     * - Client ko HTTP 400 aur `ApiResponse<ApiError>` milega jisme `subErrors` me validation messages honge.
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<?>> handleMethodArgumentNotValid(MethodArgumentNotValidException exception) {
        List<String> errors = exception
                .getBindingResult()
                .getAllErrors()
                .stream()
                .map(error -> error.getDefaultMessage())
                .collect(Collectors.toList());

        ApiError apiError = ApiError.builder()
                .status(HttpStatus.BAD_REQUEST)
                .message("Input Validation Failed")
                .subErrors(errors)
                .build();
        return buildErrorResponseEntity(apiError);
    }


    /**
     * buildErrorResponseEntity
     * <p>
     * Hinglish:
     * - Helper method jo `ApiError` ko `ApiResponse<ApiError>` me wrap karta hai aur appropriate HTTP status set karta hai.
     * - Yahan hum `new ApiResponse<>(apiError)` use karte hain taaki response body standardized rahe.
     * <p>
     * Behavior:
     * - Returns ResponseEntity with body `ApiResponse<ApiError>` and HTTP status from `apiError`.
     */
    private ResponseEntity<ApiResponse<?>> buildErrorResponseEntity(ApiError apiError) {
        return new ResponseEntity<>(new ApiResponse<>(apiError),
                apiError.getStatus());
    }

}