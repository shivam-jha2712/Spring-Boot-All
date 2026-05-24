package com.shivamjha2712.LearningRESTAPIs.advices;

import lombok.Builder;
import lombok.Data;
import org.springframework.http.HttpStatus;

import java.util.List;

/**
 * API error response object jo clients ko API errors ke liye standardized format mein bheja jaata hai.
 * Yeh class exception handling mein use hoti hai taaki har error ko consistent format mein return kiya ja sake.
 * ApiError object mein HTTP status code aur error message dono hote hain jo client ko samajh aata hai.
 */
@Builder
@Data // This was used from lombok to use getters and setters wala logic.
public class ApiError {

    /**
     * HTTP status code jo error ko represent karta hai.
     * Jaise 404 NOT_FOUND, 500 INTERNAL_SERVER_ERROR, etc.
     */
    private HttpStatus status;

    /**
     * Error ka descriptive message jo user ko batata hai ki kya problem hai.
     * Yeh message easy language mein hota hai taaki client samajh sake.
     */
    private String message;

    /**
     * Yeh errors ko like ek list of strings ke form mei store krne ke liye use hua hai.
     * Aur usmei kya kya bana hai uske liye bataya gaya hai
     */
    private List<String> subErrors;

}