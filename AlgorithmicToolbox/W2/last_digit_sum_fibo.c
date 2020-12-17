#include <stdio.h>

int last_digit_fibo_sum( long long n){ // +[0 1 ...... n]
    int lista[2] = {0 , 1}; //Para ir intercambiando
    int aux = 0;
    if ( n == 0){ //pero ya definimos 0 o 1
        return 0;
    } else if( n == 1){
        return 1;
    } 
    else {
        for (long long i = 0; i < n-1; i++){
            int fibo = (lista[0]+lista[1]) %10;
            aux += lista[0]; 
            lista[0] = lista[1];
            lista[1] = fibo;
        }
    }
    return (aux + lista[0] + lista[1]) % 10;
    
}

int main(){
    long long n;
    if(scanf("%lld",&n)){};
    int k = last_digit_fibo_sum( n % 60 ) ;
    printf("%d\n", k); //NO quiero castear
    return 0;
    //832564823476
}