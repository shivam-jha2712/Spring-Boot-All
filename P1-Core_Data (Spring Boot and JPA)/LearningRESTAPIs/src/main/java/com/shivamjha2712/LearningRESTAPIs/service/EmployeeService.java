package com.shivamjha2712.LearningRESTAPIs.service;

import com.shivamjha2712.LearningRESTAPIs.dto.EmployeeDto;
import com.shivamjha2712.LearningRESTAPIs.entites.EmployeeEntity;
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
        EmployeeEntity employeeEntity = employeeRepository.findById(employeeId).orElse(new EmployeeEntity());
        modelMapper.map(updatedEmployee, employeeEntity); // Create an employee entity from the updated employee DTO object that is being sent by the client.
//      employeeEntity.setId(employeeId); // Also for the given entity setId for the given employee. -> This is removed taaki jo generated value se khud se generate ho raha hai na id woh generate hota rahe and fase nahi.
        EmployeeEntity savedEmployeeEntity = employeeRepository.save(employeeEntity); // Save the employeeEntity insite the database using repository.
        return modelMapper.map(savedEmployeeEntity, EmployeeDto.class); // Map and convert the savedEmployeeEntity back to the EmployeeDto class.
    }

    public boolean deleteEmployeeById(Long employeeId) {
        boolean employeeExists = employeeRepository.existsById(employeeId);
        if (!employeeExists) {
            return false;
        }
        employeeRepository.deleteById(employeeId); // if does then delete that given employee.
        return true;

    }

    public EmployeeDto patchEmployeeById(Map<String, Object> updatesForPatch, Long employeeId) {
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
