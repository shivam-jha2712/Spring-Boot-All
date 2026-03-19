package com.shivamjha2712.LearningRESTAPIs.controller;

import com.shivamjha2712.LearningRESTAPIs.dto.EmployeeDto;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;

@RequestMapping(path = "/getEmployee")
// This could also be used solely as the parent context which could be used as the main endpoint of url path.
// Followed by the paths that are being used like "/{employeeId}"
// This is used to make this class as a controller and to handle the incoming request and send the response back to the client.
@RestController
// This is also a shorthand for @Controller and @ResponseBody thus it returns to JSON/XML directly to the response Body
public class EmployeeController {

    // This is a type of @RequestMapping annotation that is used by Controller methods. It has various attributes to match URL, HTTP method, request params, headers and media types as well.
//    @GetMapping(path = "/getEmployee")
//    public String getMyEmployeeName(){
//        return "Employee Name : Shivam Jha";
//    }

    //  @GetMapping(path = "/getEmployee/{employeeId}") - This was used when @RequestMapping was not used.
    @GetMapping(path = "/{employeeId}")
    public EmployeeDto getEmployeeById(@PathVariable Long employeeId) {
        return new EmployeeDto(employeeId, "Shivam", "shivam@gmail.com", 24, LocalDate.of(2020, 1, 1), true);
    }

    //  @GetMapping(path = "/getEmployee") // And this was used when the @RequestMapping was not being used.
    @GetMapping
    // This does not need a path as the /getEmployee is the parent path and is provided under @RequestMapping annotations.
    public String getAllEmployees(@RequestParam(required = false, name = "inputAge") Integer age,
                                  @RequestParam(required = false) String sortBy) {
        return "Hi age " + age + " " + sortBy;
    }

    /**
     * Also the difference between @PathVariable and @RequestParam is that:
     * 1. If you need to have a mandatory parameter you must be using @PathVariable that make sure that the user has to add the input as the request path itself.
     * 2. Whereas @RequestParam is used when you don't need the input parameters in the path to be absolutely mandatory and thus it becomes useful when you don't need absolute parameters to get the job done.
     * 3. The limitations of this is that you can only send small chunks of data in the URL and thus to pass complex data you need
     * a different annotations "@RequestBody" which will be used to bind the HTTP request body to a Java Object.
     */

    /**
     * 1. Now you can set for Post requests and Put requests and other requests but by default any request made via a browser is always a Get request.
     * 2. Thus, to have a POST/PUT/UPDATE/DELETE request functioning and see them working you need to use apps like Postman and ThunderClient for running your requests.
     *
     *
     */

    @PostMapping(path = "/addEmployee")
    public EmployeeDto createEmployee(@RequestBody EmployeeDto inputEmployee) {
        inputEmployee.setId(100L);
        return inputEmployee;
    }

    @PutMapping
    public String updateEmployee() {
        return "Hello from PUT Request";
    }

}
