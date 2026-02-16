package com.vanna.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import jakarta.validation.constraints.NotBlank;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class TrainSQLRequest {
    @NotBlank(message = "Question is required")
    private String question;
    
    @NotBlank(message = "SQL is required")
    private String sql;
}
