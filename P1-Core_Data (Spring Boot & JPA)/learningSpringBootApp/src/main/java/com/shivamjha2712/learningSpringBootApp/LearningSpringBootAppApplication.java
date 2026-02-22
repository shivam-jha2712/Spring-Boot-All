package com.shivamjha2712.learningSpringBootApp;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class LearningSpringBootAppApplication implements CommandLineRunner {

	public static void main(String[] args) {
		SpringApplication.run(LearningSpringBootAppApplication.class, args);
	}

	//	private RazorpayPaymentService paymentService = new RazorpayPaymentService(); - This is tight coupling and hence it is not the most suitable way to call an object.
//	private RazorpayPaymentService paymentService;
	//	A dependency has been injected by creating a constructor of the parent class with the given bean as a parameter which means
	//	that whenever the object of the parent class is created to run it, you will need the bean as well and
	// it will not work unless and un till the given Bean is instantiated.
//	public LearningSpringBootAppApplication(RazorpayPaymentService paymentService) {
//		this.paymentService = paymentService; // This form of Dependency Injection is called as Constructor Dependency Injection.
//	}

//	Another way to perform Dependency Injection is via Field Injection with the help of an Annotation - (@Autowired) - But it has its limitations
	@Autowired
	private RazorpayPaymentService paymentService;

//	The downside of using @Autowired is you cannot mark it as final. Like if you do it will show as an error. So if in case you want to create DI for something
//	Which needs not be changed you need to use Constructor DI then Field DI(@Autowired).



//This method runs when everything is done, when Application Context is created - if something is said above of SpringBootApp
// then it might cause and issue + added to that since main method is static every method further down needs to be static
//	Here it is not the same.- And it is added by implementing CommandLineRunner Interface.
	@Override
	public void run(String... args) throws Exception {
	String payment = paymentService.pay();
	System.out.println("Payment Done: "+payment);
	}
}
