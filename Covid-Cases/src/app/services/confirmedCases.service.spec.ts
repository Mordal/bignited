import { TestBed } from '@angular/core/testing';

import { ConfirmedCasesService } from './confirmedCases.service';

describe('confirmedCasesService', () => {
  let service: ConfirmedCasesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ConfirmedCasesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
