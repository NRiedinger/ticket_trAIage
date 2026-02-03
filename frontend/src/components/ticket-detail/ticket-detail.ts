import { Component, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TicketService } from '../../services/ticket-service/ticket-service';
import { Ticket } from '../../models/ticket.model';

import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { TextareaModule } from 'primeng/textarea';
import { IftaLabelModule } from 'primeng/iftalabel';
import { MessageModule } from 'primeng/message';
import { PanelModule } from 'primeng/panel';
import { TagModule } from 'primeng/tag';
import { SkeletonModule } from 'primeng/skeleton';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';
import { SelectButtonModule } from 'primeng/selectbutton';

@Component({
    selector: 'app-ticket-detail',
    imports: [
        CommonModule,
        FormsModule,
        CardModule,
        TextareaModule,
        IftaLabelModule,
        ButtonModule,
        MessageModule,
        PanelModule,
        TagModule,
        SkeletonModule,
        ToastModule,
        SelectButtonModule,
    ],
    providers: [MessageService],
    templateUrl: './ticket-detail.html',
    styleUrl: './ticket-detail.css',
})
export class TicketDetail {
    loading = true;
    ticket = signal<Ticket | null>(null);
    reply = signal<string>('');

    suggestion_feedback_options: any[] = ['Yes', 'No'];
    suggestion_feedback!: string;

    constructor(
        private ticketService: TicketService,
        private activatedRoute: ActivatedRoute,
        private messageService: MessageService,
        private router: Router,
    ) {}

    ngOnInit() {
        this.loading = true;
        this.activatedRoute.params.subscribe((params: any) => {
            this.ticketService.getTicketById(params.id).subscribe({
                next: (data) => {
                    const ticket = data as Ticket;
                    
                    this.ticket.set(ticket);
                    this.reply.set(ticket.suggested_reply);
                    this.loading = false;

                    switch(ticket.feedback_accepted){
                        case true:
                            this.suggestion_feedback = "Yes";
                            break;
                        case false:
                            this.suggestion_feedback = "No";
                            break;
                        default:
                            break;
                    }
                },
                error: (error) => {
                    this.showError('Failed load ticket :(');
                    this.loading = false;
                },
            });
        });
    }

    onFeedbackClick(event: any) {
        const id = this.ticket()?.id;
        if (!id) {
            this.showError('Failed to submit feedback :(');
            return;
        }

        let feedback;
        switch (event.value) {
            case 'Yes':
                feedback = true;
                break;
            case 'No':
                feedback = false;
                break;
            case null:
            default:
                feedback = null;
                break;
        }
        this.ticketService.setTicketSuggestionFeedback(id, feedback).subscribe({
            next: (data) => {
            },
            error: (error) => {
                this.showError('Failed to submit feedback :(');
            },
        });
    }

    getPrioritySeverity(prio: string | undefined) {
        switch (prio) {
            default:
            case 'Low':
                return 'success';
            case 'Medium':
                return 'warn';
            case 'High':
                return 'danger';
        }
    }

    onSend() {
        const url = `mailto:${this.ticket()?.from_email}?subject=Re: ${this.ticket()?.subject}&body=${this.reply()}`;
        window.open(url, '_self');
    }

    onNavigateBack() {
        this.router.navigate(['/tickets']);
    }

    showError(message: string) {
        this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: message,
        });
    }
}
