package com.shivamjha2712.learningSpringBootApp;

import org.springframework.stereotype.Component;

//import org.springframework.stereotype.Repository;
//import org.springframework.stereotype.Service;
//import org.springframework.web.bind.annotation.RestController;

//@Service
//@Repository
//@RestController
// These above used annotations are also either stereotype annotations that have the same meaning of that of @Component.
// They can also be used as alias for @Component as it works the same way for creation of Bean - and thus leading to IOC. (Inversion of Control)

@Component
public class StripePaymentService implements  PaymentService{
    @Override
    public String pay() {
        String payment = "Stripe Payment";
        System.out.println("Payment from :" + payment);
        return payment;
    }
}
