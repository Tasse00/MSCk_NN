SUBROUTINE LECT_C
    !READ NARROW BAND DATAS :: BAND CENTERS
    !CREATE CLUSTER FILENAMES
    USE MSCK_CO2
    IMPLICIT NONE
    201 FORMAT('../../../../NEW CLUST 27T 25C FOR HUANGSIYUAN/CO2/CDSD_CLUST_',I3,'CM_1')    
    202 FORMAT('../../../../NEW CLUST 27T 25C FOR HUANGSIYUAN/CO2/CDSD_CLUST_',I4,'CM_1')    
    OPEN(2,FILE='WVNB.DAT')
    DO IBAND=1,NBBAND
        READ(2,*) NBDAT(IBAND)
        NUMEAN=NBDAT(IBAND)
        IF(NUMEAN.LT.1000) WRITE(INFILE(IBAND),201) NUMEAN
        IF(NUMEAN.GE.1000) WRITE(INFILE(IBAND),202) NUMEAN
        ! print *, INFILE
        ! read(*,*)
        ! if (NUMEAN < 1000) then
        !     print 201, NUMEAN
        ! else
        !     print 202, NUMEAN
        ! endif
    END DO
    CLOSE(2)
    !END READ NARROW BAND CENTERS
END SUBROUTINE LECT_C
    
SUBROUTINE LECT_CDATA(JBAND)
    !READ CLUSTER DATA
    USE MSCK_CO2
    IMPLICIT NONE
    INTEGER JBAND
    NUMEAN=NBDAT(JBAND)
    WRITE(*,*) NUMEAN
    OPEN(1000,FILE=INFILE(JBAND))
    DO INU=1,NBNU
        READ(1000,110) NULOC(INU),(KLOC(INU,ITG,1),ITG=1,NTG),GROUPINDEX(INU)
        110 FORMAT(49(E20.10,1X),I3)
    ENDDO
END SUBROUTINE LECT_CDATA

	SUBROUTINE DELTACALC
	USE MSCK_CO2
	IMPLICIT NONE
    INTEGER INDEX
    !INIT
    DO INU=1,NBNU
    DO IGROUP=1,NBGROUP
    DELTA(IGROUP,INU)=0.D0
    END DO
    END DO
    !DELTA CALC
    DO INU=1,NBNU
    INDEX=GROUPINDEX(INU)
    DELTA(INDEX,INU)=1.D0
    END DO
    !END DELTA CALC
    END SUBROUTINE DELTACALC

SUBROUTINE KMINMAX
    USE MSCK_CO2
    IMPLICIT NONE    
    DO IGROUP=1,NBGROUP
        KMIN(IGROUP)=1.D20
        KMAX(IGROUP)=-1.D0
        DO INU=1,NBNU
            IF(KLOC(INU,ITREF,IXREF).LE.KMIN(IGROUP).AND.GROUPINDEX(INU).EQ.IGROUP) KMIN(IGROUP)=KLOC(INU,ITREF,IXREF)
            IF(KLOC(INU,ITREF,IXREF).GE.KMAX(IGROUP).AND.GROUPINDEX(INU).EQ.IGROUP) KMAX(IGROUP)=KLOC(INU,ITREF,IXREF)
        END DO
    END DO
END SUBROUTINE KMINMAX

    SUBROUTINE CLUSTERSIZE
	USE MSCK_CO2
	IMPLICIT NONE    
    DO IGROUP=1,NBGROUP
    SIZEGROUP(IGROUP)=0.D0
    END DO
    DO IGROUP=1,NBGROUP
    DO INU=1,NBNU
    SIZEGROUP(IGROUP)=SIZEGROUP(IGROUP)+DELTA(IGROUP,INU)
    END DO
    END DO
    END SUBROUTINE CLUSTERSIZE

    SUBROUTINE INDEXX(N,ARR,INDX)
    INTEGER N,INDX(N),M,NSTACK
    DOUBLE PRECISION ARR(N)
    PARAMETER (M=7,NSTACK=50)
    !INDEXES AN ARRAY ARR(1:N), I.E., OUTPUTS THE ARRAY INDX(1:N) SUCH THAT ARR(INDX(J))
    !IS IN ASCENDING ORDER FOR J = 1;2; : : :;N. THE INPUT QUANTITIES N AND ARR ARE NOT CHANGED.
    INTEGER I,INDXT,IR,ITEMP,J,JSTACK,K,L,ISTACK(NSTACK)
    DOUBLE PRECISION A
    DO  J=1,N
    INDX(J)=J
    ENDDO
    JSTACK=0
    L=1
    IR=N
    1 IF(IR-L.LT.M)THEN
    DO J=L+1,IR
    INDXT=INDX(J)
    A=ARR(INDXT)
    DO I=J-1,L,-1
    IF(ARR(INDX(I)).LE.A)GOTO 2
    INDX(I+1)=INDX(I)
    ENDDO 
    I=L-1
    2 INDX(I+1)=INDXT
    ENDDO
    IF(JSTACK.EQ.0)RETURN
    IR=ISTACK(JSTACK)
    L=ISTACK(JSTACK-1)
    JSTACK=JSTACK-2
    ELSE
    K=(L+IR)/2
    ITEMP=INDX(K)
    INDX(K)=INDX(L+1)
    INDX(L+1)=ITEMP
    IF(ARR(INDX(L)).GT.ARR(INDX(IR)))THEN
    ITEMP=INDX(L)
    INDX(L)=INDX(IR)
    INDX(IR)=ITEMP
    ENDIF
    IF(ARR(INDX(L+1)).GT.ARR(INDX(IR)))THEN
    ITEMP=INDX(L+1)
    INDX(L+1)=INDX(IR)
    INDX(IR)=ITEMP
    ENDIF
    IF(ARR(INDX(L)).GT.ARR(INDX(L+1)))THEN
    ITEMP=INDX(L)
    INDX(L)=INDX(L+1)
    INDX(L+1)=ITEMP
    ENDIF
    I=L+1
    J=IR
    INDXT=INDX(L+1)
    A=ARR(INDXT)
    3 CONTINUE
    I=I+1
    IF(ARR(INDX(I)).LT.A)GOTO 3
    4 CONTINUE
    J=J-1
    IF(ARR(INDX(J)).GT.A)GOTO 4
    IF(J.LT.I)GOTO 5
    ITEMP=INDX(I)
    INDX(I)=INDX(J)
    INDX(J)=ITEMP
    GOTO 3
    5 INDX(L+1)=INDX(J)
    INDX(J)=INDXT
    JSTACK=JSTACK+2
    IF(JSTACK.GT.NSTACK)PAUSE 'NSTACK TOO SMALL IN INDEXX'
    IF(IR-I+1.GE.J-L)THEN
    ISTACK(JSTACK)=IR
    ISTACK(JSTACK-1)=I
    IR=J-1
    ELSE
    ISTACK(JSTACK)=J-1
    ISTACK(JSTACK-1)=L
    L=I
    ENDIF
    ENDIF
    GOTO 1
    END SUBROUTINE INDEXX