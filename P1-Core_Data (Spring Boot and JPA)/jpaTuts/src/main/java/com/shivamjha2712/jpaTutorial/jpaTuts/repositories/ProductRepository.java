package com.shivamjha2712.jpaTutorial.jpaTuts.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<ProductEntity, Long> {
}
