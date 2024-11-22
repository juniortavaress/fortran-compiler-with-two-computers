C!==========================================================
C!                    VUHARD Subroutine
C!                Developer: Soheil Rooein
C!                          2024
C!           IWM Institute - RWTH Aachen University
C!========================================================== 

      SUBROUTINE VUHARD( 
C Read only -	
     1	nblock, jElem, kIntPt, kLayer, kSecPt, 
     2	lAnneal, stepTime, totalTime, dt, cmname,
     3	nstatev, nfieldv, nprops, 
     4	props, tempOld, tempNew, fieldOld, fieldNew,
     5	stateOld, eqps, eqpsRate,
C Write only -
     6     yield, dyieldDtemp, dyieldDeqps, stateNew )
C-----------
		INCLUDE 'vaba_param.inc'

		DIMENSION props(nprops), tempOld(nblock), tempNew(nblock),
     1   		fieldOld(nblock,nfieldv), fieldNew(nblock,nfieldv),
     2   		stateOld(nblock,nstatev), eqps(nblock), eqpsRate(nblock),
     3   		yield(nblock), dyieldDtemp(nblock), dyieldDeqps(nblock,2),
     4   		stateNew(nblock,nstatev), jElem(nblock)

		CHARACTER*80 cmname
		DOUBLE PRECISION A, B, n, C1, C2, C3, EQPLAS_Zero
		DOUBLE PRECISION k, Ts
		DOUBLE PRECISION S_static, S_Rate, Theta
C-----------
		A = 1300D2
		B = 750D1
		n = 1D-1    
		
		C1 = 90D-4
		C2 = 2.5D-8
		C3 = 6D-7
		EQPLAS_Zero = 2D-3
		
		k = 90D-8
		Ts = 900.0D4
C-----------
		DO 100 km = 1,nblock			
			S_static = A+B*(eqps(km)**n)
			S_Rate   = 1D0+(C1+C2*DEXP(C3*tempNew(km)))*DLOG(eqpsRate(km)/EQPLAS_Zero)
			Theta	   = 1D0/(1D0+DEXP(k*(tempNew(km)-Ts)))	
C-----------------			
			IF (eqpsRate(km) >= EQPLAS_Zero) THEN				
				dyieldDeqps(km,2) = S_static*Theta*(C1+C2*DEXP(C3*tempNew(km)))/eqpsRate(km)
			ELSE
				S_Rate = 1.0
				dyieldDeqps(km,2) = 0
			END IF
				
			yield(km)  = S_static*S_Rate*Theta
			dyieldDeqps(km,1) = (B*n*eqps(km)**(n-1))*S_Rate*Theta
			dyieldDtemp(km) = S_static*( (C2*C3*DEXP(C3*tempNew(km))*DLOG(eqpsRate(km)/EQPLAS_Zero))/(1+DEXP(k*(tempNew(km)-Ts)))
     1	          - (S_Rate*DEXP(k*(tempNew(km)-Ts))*k)/(1+DEXP(k*(tempNew(km)-Ts)))**2 )
C-----------------
			stateNew(km,1) = yield(km)
			stateNew(km,2) = S_static
			stateNew(km,3) = S_Rate
			stateNew(km,4) = Theta
			stateNew(km,5) = eqpsRate(km)

  100 	CONTINUE
		
      RETURN
      END