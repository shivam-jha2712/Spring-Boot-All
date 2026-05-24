package com.shivamjha2712.LearningRESTAPIs.exceptions;

/**
 * Custom exception thrown when a requested resource is not found.
 * Extends RuntimeException to make it an unchecked exception.
 * This exception is used throughout the application to signal that a client
 * requested resource (e.g., an employee with a specific ID) does not exist.
 */
public class ResourceNotFoundException extends RuntimeException {

    /**
     * Constructor that creates a new ResourceNotFoundException with a descriptive error message.
     *
     * @param message Descriptive error message explaining what resource was not found
     */
    public ResourceNotFoundException(String message) {
        // constructor was needed to be created here.
        super(message);
    }
}
