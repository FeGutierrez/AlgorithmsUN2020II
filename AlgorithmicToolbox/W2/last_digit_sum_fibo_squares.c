#include <stdio.h>

int last_digit_fibo( long long n){ // +[0 1 ...... n]
    int lista[2] = {0 , 1}; //Para ir intercambiando
    if ( n == 0){ //pero ya definimos 0 o 1
        return 0;
    } else if( n == 1){
        return 1;
    } 
    else {
        for (long long i = 0; i < n-1; i++){
            int fibo = (lista[0]+lista[1]) %10;
            lista[0] = lista[1];
            lista[1] = fibo;
        }
    }
    return (lista[1]) % 10;
}

int main(){
    long long n;
    if(scanf("%lld",&n)){};    
    int k = last_digit_fibo( n % 60 ) ;
    int l = last_digit_fibo( (n-1) % 60 ) ;
    int z = ((k + l) * k ) % 10;
    printf("%d\n", z);
    return 0;
    //832564823476
    //1234567890
}