import { TestBed } from '@angular/core/testing';

import { MyApiService } from './my-api.service';

describe('MyApiService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: MyApiService = TestBed.get(MyApiService);
    expect(service).toBeTruthy();
  });
});
