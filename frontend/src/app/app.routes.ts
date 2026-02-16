import { Routes } from '@angular/router';
import { TrainComponent } from './components/train/train.component';
import { AskComponent } from './components/ask/ask.component';

export const routes: Routes = [
  { path: '', redirectTo: '/train', pathMatch: 'full' },
  { path: 'train', component: TrainComponent },
  { path: 'ask', component: AskComponent }
];
