package com.shivamjha2712.LearningRESTAPIs.repository;

import com.shivamjha2712.LearningRESTAPIs.entites.EmployeeEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface EmployeeRepository extends JpaRepository<EmployeeEntity, Long> {
    // This is going to be the interface that is going to be used to interact with the database and thus it is going to be used by the service layer to perform the operations on the database.
    // The JpaRepository is a JPA specific extension of Repository. It contains the full API of CrudRepository and PagingAndSortingRepository. Thus, it contains all the methods for performing CRUD operations and pagination and sorting operations on the database.
    // The first parameter is the type of the entity and the second parameter is the type of the primary key of the entity.

    List<EmployeeEntity> findByName(String name);

}
