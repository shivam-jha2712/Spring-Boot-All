package com.shivamjha2712.LearningRESTAPIs.advices;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * ApiResponse<T>
 * <p>
 * Hinglish explanation:
 * - Yeh generic response wrapper hai jo successful response ko ek consistent shape mein
 * client ko bhejne ke liye use hota hai.
 * - Structure: { timestamp, data, error }
 * - agar request successful hai to `data` filled hoga aur `error` null rahega
 * - agar koi exception hua to `error` filled hoga aur `data` null rahega
 * <p>
 * Use-case:
 * - Controller ya ResponseBodyAdvice se return karne ke liye.
 * - Agar tum GlobalResponseHandler mein DTO-based wrapping karna chahte ho, to is class ko use karo.
 */
@Data
public class ApiResponse<T> {

    @JsonFormat(pattern = "dd-MM-yyyy | HH:mm:ss")
    /**
     * timestamp:
     * - response create hone ka samay. automatic constructor mein set hota hai.
     * - helpful for debugging aur client-side logs.
     */
    private LocalDateTime timestamp;

    /**
     * data:
     * - successful response ka payload. generic type T hai taaki kisi bhi DTO/list ko hold kar sake.
     * - success case mein yahan actual result aayega.
     */
    private T data;

    /**
     * error:
     * - agar koi exception ya validation error hua ho to yahan `ApiError` object aayega.
     * - success case mein yeh null hona chahiye.
     */
    private ApiError error;

    /**
     * Default constructor:
     * - timestamp ko current time se initialize karta hai.
     * - isse har response mein timestamp available rahega automatically.
     */
    public ApiResponse() {
        this.timestamp = LocalDateTime.now();
    }

    /**
     * Success constructor:
     * - Jab successful response bhejna ho to use karo.
     * - Automatically timestamp set hota hai aur data populate hota hai.
     *
     * @param data successful response payload
     */
    public ApiResponse(T data) {
        this();
        this.data = data;
    }

    /**
     * Error constructor:
     * - Jab exception handler se error bhejna ho to use karo.
     * - Timestamp set ho jaata hai aur error field populate hota hai.
     *
     * @param error ApiError object describing the failure
     */
    public ApiResponse(ApiError error) {
        this();
        this.error = error;
    }
}