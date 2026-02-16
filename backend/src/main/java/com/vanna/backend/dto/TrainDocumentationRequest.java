package com.vanna.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import jakarta.validation.constraints.NotBlank;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class TrainDocumentationRequest {
    @NotBlank(message = "Documentation is required")
    private String documentation;
}
