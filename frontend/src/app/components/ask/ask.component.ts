import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VannaService } from '../../services/vanna.service';

@Component({
  selector: 'app-ask',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './ask.component.html',
  styleUrl: './ask.component.css'
})
export class AskComponent {
  question = '';
  loading = false;
  errorMessage = '';
  
  result: any = null;

  constructor(private vannaService: VannaService) {}

  askQuestion() {
    if (!this.question.trim()) {
      this.errorMessage = 'Please enter a question';
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    this.result = null;

    this.vannaService.askQuestion({ question: this.question }).subscribe({
      next: (response) => {
        this.loading = false;
        if (response.success) {
          this.result = response.data;
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

  clearResults() {
    this.result = null;
    this.question = '';
    this.errorMessage = '';
  }
}
