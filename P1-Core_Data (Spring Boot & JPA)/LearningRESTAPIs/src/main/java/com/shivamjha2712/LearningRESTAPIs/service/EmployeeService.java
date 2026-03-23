package com.shivamjha2712.LearningRESTAPIs.service;

import com.shivamjha2712.LearningRESTAPIs.dto.EmployeeDto;
import com.shivamjha2712.LearningRESTAPIs.entites.EmployeeEntity;
import com.shivamjha2712.LearningRESTAPIs.repository.EmployeeRepository;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class EmployeeService {
    // This is going to be the service layer that is going to be used to perform the business logic of the application and
    // thus it is going to be used by the controller layer to perform the operations on the database through the repository layer.

    private final EmployeeRepository employeeRepository;
    private final ModelMapper modelMapper;

    public EmployeeService(EmployeeRepository employeeRepository) {
        this.employeeRepository = employeeRepository;
        modelMapper = new ModelMapper();
    }

    // Initially, we would have used EmployeeEntity directly but after the use of modelmapper we can simply use DTO to get the correlation between both entity and DTO as well.
    public EmployeeDto getEmployeeById(Long id) {
        EmployeeEntity employeeEntity = employeeRepository.findById(id).orElse(null); //  We are using orElse to verify if we are getting the data or not and if we are not getting the data then we are going to return null.
        return modelMapper.map(employeeEntity, EmployeeDto.class);
    }

    public List<EmployeeDto> getAllEmployees() {
        List<EmployeeEntity> employeeEntities = employeeRepository.findAll();
        // Now to convert the list of employeeEntities into a list of EmployeeDTO we can use stream library and thus we can use the map function to convert each employeeEntity into employeeDTO and then collect the result into a list.
        return employeeEntities
                .stream()
                .map(employeeEntity -> modelMapper.map(employeeEntity, EmployeeDto.class))
                .collect(Collectors.toList());
    }

    public EmployeeDto createEmployee(EmployeeDto inputEmployee) {
        EmployeeEntity toSaveEntity = modelMapper.map(inputEmployee, EmployeeEntity.class); // Converting a DTO object in an entity what can be saved.
        EmployeeEntity savedEmployeeEntity = employeeRepository.save(toSaveEntity); // Saving the entity in the database and getting the saved entity back which is going to have the generated id as well.
        return modelMapper.map(savedEmployeeEntity, EmployeeDto.class); // Now the entity that will be saved needs to be converted back into a DTO object to be sent back to the client as a response.
    }
}
