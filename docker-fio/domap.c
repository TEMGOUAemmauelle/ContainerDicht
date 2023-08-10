#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define handle_error(msg) \
    do { perror(msg); exit(EXIT_FAILURE); } while (0)

int
main(int argc, char *argv[])
{
    char *addr;
    int fd;
    struct stat sb;
    off_t offset, pa_offset;
    size_t length;
    ssize_t s;

    if (argc < 3 || argc > 4) {
        fprintf(stderr, "%s fichier offset [longueur]\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    fd = open(argv[1], O_RDONLY);
    if (fd == -1)
        handle_error("open");

    if (fstat(fd, &sb) == -1)           /* Pour obtenir la taille du fichier */
        handle_error("fstat");

    offset = atoi(argv[2]);
    pa_offset = offset & ~(sysconf(_SC_PAGE_SIZE) - 1);
        /* la position de mmap() doit être alignée sur la page */

    if (offset >= sb.st_size) {
        fprintf(stderr, "L'offset dépasse la fin du fichier\n");
        exit(EXIT_FAILURE);
    }

    if (argc == 4) {
        length = atoi(argv[3]);
        if (offset + length > sb.st_size)
            length = sb.st_size - offset;
                /* Impossible d'afficher les octets en dehors du fichier */

    } else {    /* Pas de paramètre longueur
                    ==> affichage jusqu'à la fin du fichier */
        length = sb.st_size - offset;
    }

    addr = mmap(NULL, length + offset - pa_offset, PROT_READ,
                MAP_PRIVATE, fd, pa_offset);
    if (addr == MAP_FAILED)
        handle_error("mmap");
    else printf("\n fichier mapé en mémoire \n");

    /*s = write(STDOUT_FILENO, addr + offset - pa_offset, length);
    if (s != length) {
        if (s == -1)
            handle_error("write");

        fprintf(stderr, "écriture partielle");
        exit(EXIT_FAILURE);
    }*/
    printf("\n Appuie sur une touche pour arreter le mappage \n");
    getchar();



    int ok = munmap(addr, length + offset - pa_offset);
    if (ok == 0) printf("\n fichier supprimmé de la mémoire\n \n");
    close(fd);

    exit(EXIT_SUCCESS);
}