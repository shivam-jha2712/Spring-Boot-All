package com.shivamjha2712.learningSpringBootApp;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

// This is going to mark it as a Bean class - which while Component Scanning will be used and marked for Object creation when needed.
@Component
@ConditionalOnProperty(name="payment.provider", havingValue = "razorpay") // And this the Conditional On property,
// which means based on whatever incoming properties are present based on that the given payment service would be called.
public class RazorpayPaymentService implements PaymentService{
    // This thing of implements payment service is done so that a single channel is present from where the payment services
    // could be defined based on the properties that are incoming.

    @Override
    public String pay() {
        String payment = "RazorPay Payment";
        System.out.println("Payment from :" + payment);
        return payment;
    }
}
