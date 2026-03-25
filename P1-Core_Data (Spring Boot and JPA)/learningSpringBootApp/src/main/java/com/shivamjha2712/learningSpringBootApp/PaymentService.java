package com.shivamjha2712.learningSpringBootApp;

public interface PaymentService {

    String pay(); // Since it is an interface ka method hence by default it will be public and abstract.
    // And it is said to not have access modifiers and by default it is public kyunki yeh method jo class isko implements karega
    // woh hi iski body bhi define krega
}
