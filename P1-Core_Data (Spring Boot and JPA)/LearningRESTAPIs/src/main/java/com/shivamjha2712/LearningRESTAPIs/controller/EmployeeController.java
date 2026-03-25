package com.shivamjha2712.LearningRESTAPIs.controller;

import com.shivamjha2712.LearningRESTAPIs.dto.EmployeeDto;
import com.shivamjha2712.LearningRESTAPIs.service.EmployeeService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@RequestMapping(path = "/getEmployee")
// This could also be used solely as the parent context which could be used as the main endpoint of url path.
// Followed by the paths that are being used like "/{employeeId}"
// This is used to make this class as a controller and to handle the incoming request and send the response back to the client.
@RestController
// This is also a shorthand for @Controller and @ResponseBody thus it returns to JSON/XML directly to the response Body
public class EmployeeController {

    // This is a type of @RequestMapping annotation that is used by Controller methods. It has various attributes to match URL, HTTP method, request params, headers and media types as well.
/**   @GetMapping(path = "/getEmployee")
public String getMyEmployeeName(){
return "Employee Name : Shivam Jha";
}
 */


    /**
     * We can even make the conversion of Employee Entity to Employee DTO so that the modularity and seperation betweeen bothe presentation and persistance layer will remain intact.
     */

    private final EmployeeService employeeService; // The usage of service layer in controller has stripped off the usage of employee repository here.

    public EmployeeController(EmployeeService employeeService) {
        this.employeeService = employeeService;
    }


    /**
     * After the use of ModelMapper we can ditch the usage of EmployeeEntity directly as a return type and use EmployeeDto as the return type and thus we can get the correlation between both entity and DTO as well.
     *
     */
    //  @GetMapping(path = "/getEmployee/{employeeId}") - This was used when @RequestMapping was not used.
    @GetMapping(path = "/{employeeId}")
    public ResponseEntity<EmployeeDto> getEmployeeById(@PathVariable("employeeId") Long id) {
        Optional<EmployeeDto> employeeDto = employeeService.getEmployeeById(id);
        return employeeDto
                .map(employeeDto1 -> ResponseEntity.ok().body(employeeDto1))
                .orElse(ResponseEntity.notFound().build());
    }


    /*** Also the difference between @PathVariable and @RequestParam is that:
     * 1. If you need to have a mandatory parameter you must be using @PathVariable that make sure that the user has to add the input as the request path itself.
     * 2. Whereas @RequestParam is used when you don't need the input parameters in the path to be absolutely mandatory and thus it becomes useful when you don't need absolute parameters to get the job done.
     * 3. The limitations of this is that you can only send small chunks of data in the URL and thus to pass complex data you need
     * a different annotations "@RequestBody" which will be used to bind the HTTP request body to a Java Object.
     */

    //  @GetMapping(path = "/getEmployee") // And this was used when the @RequestMapping was not being used.
    @GetMapping
    // This does not need a path as the /getEmployee is the parent path and is provided under @RequestMapping annotations.
    public ResponseEntity<List<EmployeeDto>> getAllEmployees(@RequestParam(required = false, name = "inputAge") Integer age,
                                                             @RequestParam(required = false) String sortBy) {
        return ResponseEntity.ok(employeeService.getAllEmployees());
    }

    /**
     * 1. Now you can set for Post requests and Put requests and other requests but by default any request made via a browser is always a Get request.
     * 2. Thus, to have a POST/PUT/UPDATE/DELETE request functioning and see them working you need to use apps like Postman and ThunderClient for running your requests.
     *
     *
     */

    @PostMapping(path = "/addEmployee")
    public ResponseEntity<EmployeeDto> createEmployee(@RequestBody EmployeeDto inputEmployee) {
        // This can also have logic to check if this can be performed only by the admin that could be something that needs to be checked.
        // To log details associated with this method can also be added here as well.
        EmployeeDto savedEmployeeDto = employeeService.createEmployee(inputEmployee); // Saving an employee in a new DTO and if it gets successful or gets error both are below handled by ResponseEntity<>;
        return new ResponseEntity<>(savedEmployeeDto, HttpStatus.CREATED); // we are getting it created and once it is done we are passing a custom status code for creation of the employeeInside it.
    }

    @PutMapping(path = "/{employeeId}")
    public ResponseEntity<EmployeeDto> updateEmployeebyId(@RequestBody EmployeeDto updatedEmployee, @PathVariable Long employeeId) {
        return ResponseEntity.ok(employeeService.updateEmployeebyId(updatedEmployee, employeeId)); // in this only thing will throw error if not updated so no such validation needed.
    }

    @DeleteMapping(path = "/{employeeId}")
    public ResponseEntity<Boolean> deleteEmployeebyId(@PathVariable Long employeeId) {
        boolean gotDeleted = employeeService.deleteEmployeeById(employeeId); // This is going to call simply the function for deleting the employee whose Id is mentioned.
        // and the validation using boolean flag is also done over here.
        if (gotDeleted) {
            ResponseEntity.ok(true); // Checks associated to Deletion using ResponseEntity
        }
        return ResponseEntity.notFound().build();
    }

    @PatchMapping(path = "/{employeeId}")
    public ResponseEntity<EmployeeDto> patchEmployeeById(@RequestBody Map<String, Object> updates,
                                                         @PathVariable Long employeeId) {
        EmployeeDto employeeDto = employeeService.patchEmployeeById(updates, employeeId);
        if (employeeDto == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(employeeDto);
    }
}
