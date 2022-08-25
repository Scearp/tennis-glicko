#include "utils.h"
#include <stdio.h>

int main() {
    int i[6] = {5, 1, 2, 3, 4, 5};
    remove_int_from_array(3, i);
    int j;
    for (j=1; j<=i[0]; j++) {
        printf("%i\n", i[j]);
    }
    return 0;
}