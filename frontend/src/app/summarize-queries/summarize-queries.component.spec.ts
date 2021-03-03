import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SummarizeQueriesComponent } from './summarize-queries.component';

describe('SummarizeQueriesComponent', () => {
  let component: SummarizeQueriesComponent;
  let fixture: ComponentFixture<SummarizeQueriesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SummarizeQueriesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SummarizeQueriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
