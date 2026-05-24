package com.shivamjha2712.LearningRESTAPIs.service;

import com.shivamjha2712.LearningRESTAPIs.dto.EmployeeDto;
import com.shivamjha2712.LearningRESTAPIs.entites.EmployeeEntity;
import com.shivamjha2712.LearningRESTAPIs.exceptions.ResourceNotFoundException;
import com.shivamjha2712.LearningRESTAPIs.repository.EmployeeRepository;
import org.modelmapper.ModelMapper;
import org.springframework.data.util.ReflectionUtils;
import org.springframework.stereotype.Service;

import java.lang.reflect.Field;
import java.util.List;
import java.util.Map;
import java.util.Optional;
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
    public Optional<EmployeeDto> getEmployeeById(Long id) {
//        EmployeeEntity employeeEntity = employeeRepository.findById(id).orElse(null); //  We are using orElse to verify if we are getting the data or not and if we are not getting the data then we are going to return null.
//        return modelMapper.map(employeeEntity, EmployeeDto.class);
        Optional<EmployeeEntity> employeeEntity = employeeRepository.findById(id);
        return employeeEntity.map(employeeEntity1 -> modelMapper.map(employeeEntity1, EmployeeDto.class));
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

    public EmployeeDto updateEmployeebyId(EmployeeDto updatedEmployee, Long employeeId) {
        // Step 1: pehle check karo employee exist karta hai ya nahi
        isExistsEmployeeById(employeeId); // check if employee with given id exists in first place or not?

        // Step 2: DTO -> Entity map karo (same style as screenshot)
        EmployeeEntity employeeEntity = modelMapper.map(updatedEmployee, EmployeeEntity.class);

        // Step 3: IMPORTANT FIX
        // Pehle issue ye tha ki mapping ke baad id null ho rahi thi, Hibernate error de raha tha:
        // "Identifier ... altered from <id> to null"
        // Isliye id ko explicitly path variable se set kar rahe hain.
        employeeEntity.setId(employeeId);

        // Step 4: save and return response DTO
        EmployeeEntity savedEmployeeEntity = employeeRepository.save(employeeEntity);
        return modelMapper.map(savedEmployeeEntity, EmployeeDto.class);
    }

    // Function to check if employee with the given id exists or not and if it does not exist then throw an exception that employee with the given id is not found.
    public boolean isExistsEmployeeById(Long employeeId) {
        boolean exists = employeeRepository.existsById(employeeId);
        if (!exists) {
            throw new ResourceNotFoundException("Employee with id: " + employeeId + " not found");
        }
        return true;
    }

    public boolean deleteEmployeeById(Long employeeId) {
        isExistsEmployeeById(employeeId); // check if employee with given id exists in first place or not?
        employeeRepository.deleteById(employeeId); // if does then delete that given employee.
        return true;

    }

    public EmployeeDto patchEmployeeById(Map<String, Object> updatesForPatch, Long employeeId) {
        isExistsEmployeeById(employeeId); // check if employee with given id exists in first place or not?
        EmployeeEntity employeeEntity = employeeRepository.findById(employeeId).orElse(null);
        updatesForPatch.forEach((field, value) -> {
            Field fieldToBeUpdated = ReflectionUtils.getRequiredField(EmployeeEntity.class, field); // Reflections is a Utility which is used to create a reflection of the DTO that has been created and make updates on that. And then push that reflection in the repository.
            fieldToBeUpdated.setAccessible(true); // setting the fields that needs to be updated as publicly accessible so they can be updated.
            ReflectionUtils.setField(fieldToBeUpdated, employeeEntity, value); // fields that are supposed to be updated are passed in the employeeEntity with the values that are in the updatesForPatch map.
        });
        employeeRepository.save(employeeEntity); // saving the employeeEntity with the updated changes.
        return modelMapper.map(employeeEntity, EmployeeDto.class); // using modelMapper to convert the employeeEntity back to employeeDTO.

    }
}
