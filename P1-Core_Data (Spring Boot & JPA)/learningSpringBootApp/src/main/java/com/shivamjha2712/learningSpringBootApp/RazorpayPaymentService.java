package com.shivamjha2712.learningSpringBootApp;

import org.springframework.stereotype.Component;

@Component
// This is going to mark it as a Bean class - which while Component Scanning will be used and marked for Object creation when needed.
public class RazorpayPaymentService implements PaymentService{

    @Override
    public String pay() {
        String payment = "RazorPay Payment";
        System.out.println("Payment from :" + payment);
        return payment;
    }
}
