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
 * Global exception handler for the REST API.
 * Centralized handling of exceptions across all controllers.
 * Converts domain exceptions into standardized API error responses.
 * Uses Spring's @RestControllerAdvice to intercept exceptions and provide
 * consistent error formatting to API clients.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Handles ResourceNotFoundException and returns a standardized error response.
     * Converts the domain exception into an ApiError object with HTTP 404 status.
     *
     * @param exception The ResourceNotFoundException that was thrown
     * @return ResponseEntity containing ApiError with HTTP 404 (NOT_FOUND) status
     */
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiError> handleResourceNotFound(ResourceNotFoundException exception) {
        ApiError apiError = ApiError.builder()
                .status(HttpStatus.NOT_FOUND)
                .message(exception.getMessage())
                .build();
        return new ResponseEntity<>(apiError, HttpStatus.NOT_FOUND);
    }

    //Example of sample error to justify how to create and add your own version of custom exceptions for your use case and then handle it in the global exception handler to send the response back to the client in a standardized format.
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiError> handleInternalServerError(Exception exception) {
        ApiError apiError = ApiError.builder()
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .message(exception.getMessage())
                .build();
        return new ResponseEntity<>(apiError, HttpStatus.INTERNAL_SERVER_ERROR);
    }
    // This is also going to give you only the bindedresult of the error which is not going to be very much understandable by any one other than who knows the system thus to handle that we can create a custom exception for the validation error and then handle that in the global exception handler to send the response back to the client in a standardized format.

    // The Custom Exception of dealing with those validation error can be justified as follows:
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiError> handleMethodArgumentNotValid(MethodArgumentNotValidException exception) {
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
        return new ResponseEntity<>(apiError, HttpStatus.BAD_REQUEST);
    }

}