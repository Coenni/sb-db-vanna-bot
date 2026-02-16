import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VannaService } from '../../services/vanna.service';

@Component({
  selector: 'app-train',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './train.component.html',
  styleUrl: './train.component.css'
})
export class TrainComponent {
  activeTab: 'ddl' | 'documentation' | 'sql' = 'ddl';
  
  // Form models
  ddl = '';
  documentation = '';
  question = '';
  sql = '';
  
  // Response messages
  successMessage = '';
  errorMessage = '';
  loading = false;

  constructor(private vannaService: VannaService) {}

  setActiveTab(tab: 'ddl' | 'documentation' | 'sql') {
    this.activeTab = tab;
    this.clearMessages();
  }

  clearMessages() {
    this.successMessage = '';
    this.errorMessage = '';
  }

  trainDDL() {
    if (!this.ddl.trim()) {
      this.errorMessage = 'Please enter DDL';
      return;
    }

    this.loading = true;
    this.clearMessages();

    this.vannaService.trainWithDDL({ ddl: this.ddl }).subscribe({
      next: (response) => {
        this.loading = false;
        if (response.success) {
          this.successMessage = response.message;
          this.ddl = '';
        } else {
          this.errorMessage = response.message;
        }
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = 'Error: ' + (error.error?.message || error.message);
      }
    });
  }

  trainDocumentation() {
    if (!this.documentation.trim()) {
      this.errorMessage = 'Please enter documentation';
      return;
    }

    this.loading = true;
    this.clearMessages();

    this.vannaService.trainWithDocumentation({ documentation: this.documentation }).subscribe({
      next: (response) => {
        this.loading = false;
        if (response.success) {
          this.successMessage = response.message;
          this.documentation = '';
        } else {
          this.errorMessage = response.message;
        }
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = 'Error: ' + (error.error?.message || error.message);
      }
    });
  }

  trainSQL() {
    if (!this.question.trim() || !this.sql.trim()) {
      this.errorMessage = 'Please enter both question and SQL';
      return;
    }

    this.loading = true;
    this.clearMessages();

    this.vannaService.trainWithSQL({ question: this.question, sql: this.sql }).subscribe({
      next: (response) => {
        this.loading = false;
        if (response.success) {
          this.successMessage = response.message;
          this.question = '';
          this.sql = '';
        } else {
          this.errorMessage = response.message;
        }
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = 'Error: ' + (error.error?.message || error.message);
      }
    });
  }
}
