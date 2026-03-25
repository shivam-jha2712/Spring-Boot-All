package com.shivamjha2712.LearningRESTAPIs.dto;

import java.time.LocalDate;

//@Data  // The use of this annotation is to remove the creation of getters and setting and constructors and simply get the data from lombok
public class EmployeeDto {
    private Long id;
    private String name;
    private String email;
    private Integer age;
    private LocalDate dateOfJoining;
    private Boolean active;

    public EmployeeDto() {
    }

    public EmployeeDto(Long id, String name, String email, Integer age, LocalDate dateOfJoining, Boolean active) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.age = age;
        this.dateOfJoining = dateOfJoining;
        this.active = active;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public LocalDate getDateOfJoining() {
        return dateOfJoining;
    }

    public void setDateOfJoining(LocalDate dateOfJoining) {
        this.dateOfJoining = dateOfJoining;
    }

    public Boolean getActive() {
        return active;
    }

    public void setActive(Boolean active) {
        this.active = active;
    }
    /**
     * Learn about Wrapper "Integer" "Boolean" "String" - inplace of int, boolean and str -
     * to have no issue while passing data in the request body and to have the flexibility of having null values as well.
     * */

    /**
     * Why should I not use isActive and use active as my name of parameter?
     * <p>
     * `active` is fine as a parameter name.
     * <p>
     * - `isActive()` is the standard JavaBean getter name for a `boolean` field.
     * - `setActive(boolean active)` is also standard, and the parameter name should usually match the field name.
     * - `isActive` as a parameter name is allowed, but it is less clear because it looks like a method name rather than a value.
     * <p>
     * So, keep:
     * - field: `active`
     * - getter: `isActive()`
     * - setter parameter: `active`
     * <p>
     * That is the usual and clearest convention.
     */

}
