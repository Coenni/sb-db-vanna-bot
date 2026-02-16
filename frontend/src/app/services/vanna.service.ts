import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ApiResponse {
  success: boolean;
  message: string;
  data?: any;
}

export interface TrainDDLRequest {
  ddl: string;
}

export interface TrainDocumentationRequest {
  documentation: string;
}

export interface TrainSQLRequest {
  question: string;
  sql: string;
}

export interface AskQuestionRequest {
  question: string;
}

@Injectable({
  providedIn: 'root'
})
export class VannaService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  trainWithDDL(request: TrainDDLRequest): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/train/ddl`, request);
  }

  trainWithDocumentation(request: TrainDocumentationRequest): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/train/documentation`, request);
  }

  trainWithSQL(request: TrainSQLRequest): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/train/sql`, request);
  }

  askQuestion(request: AskQuestionRequest): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(`${this.apiUrl}/ask`, request);
  }

  getTrainingData(): Observable<ApiResponse> {
    return this.http.get<ApiResponse>(`${this.apiUrl}/training-data`);
  }
}
