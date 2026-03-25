package com.shivamjha2712.LearningRESTAPIs.configs;


import org.modelmapper.ModelMapper;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MapperConfig {
    // This is going to be the configuration class that is going to be used to configure the mapper that is going to be used to map the data from the entity to the DTO and vice versa.
    // We are going to use ModelMapper as our mapper and thus we need to create a bean for it in this configuration class.

    @Bean
    public ModelMapper getModelMapper() {
        return new ModelMapper();
    }
}
