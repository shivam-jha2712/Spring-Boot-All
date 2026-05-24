package com.shivamjha2712.LearningRESTAPIs.entites;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;

@Entity
/**
 * The difference between an Entity and DTO is that Entity is used to mark how a data will be stored in a Database
 * Whereas the DTO is used to mark how the data will be sent to the client and how it will be received from the client.
 * Thus, the Entity is used for Database and DTO is used for Client.
 */
@Getter // This is done using the Lombok dependency.
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "employees")
public class EmployeeEntity {


    @Id // This is going to determine what is going to be a primary key inside any entity.
    @GeneratedValue(strategy = GenerationType.AUTO)
    // This is going to determine that the value of the primary key is going to be generated automatically by the database and thus we don't need to set it manually. As in case of SQL it is set as auto increment.
    private Long id;
    private String name;
    private String email;
    private Integer age;
    private String role;
    private Double salary;
    private LocalDate dateOfJoining;
    private Boolean active;
}
