package com.shivamjha2712.LearningRESTAPIs.annotations;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;

import java.lang.annotation.*;

@Documented
@Constraint(validatedBy = EmployeeRoleValidator.class)
@Target({ElementType.FIELD, ElementType.PARAMETER, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface EmployeeRoleValidation {
    String message() default "Role of Employee can be USER or ADMIN or CREATOR";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}