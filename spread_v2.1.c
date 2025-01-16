#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_TEAMS 32
#define MAX_WEEKS 17
#define MAX_GAMES 100

typedef struct {
    int week;
    char team1[4];
    char team2[4];
    int spread;
} Game;

typedef struct {
    int week;
    int spread;
    char team[4];
} Pick;

Game games[MAX_GAMES];
int total_games = 0;

char already_picked[MAX_TEAMS][4] = {"PHI", "SF", "DAL", "CIN", "WAS", "MIA", "BUF", "BAL", "CLE", "SEA", "DET", "MIN", "KC", "PIT", "LAR"};
int weeks_picked[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
int total_already_picked = 11;
int total_weeks_picked = 11;

int remaining_weeks[MAX_WEEKS];
int total_remaining_weeks = 0;

Pick possible_picks[MAX_GAMES];
int total_possible_picks = 0;

Pick best_set[MAX_WEEKS];
int best_min_spread = 0;
int best_total_spread = 0;

// Helper function to check if a team is already picked
int is_already_picked(const char *team) {
    for (int i = 0; i < total_already_picked; i++) {
        if (strcmp(already_picked[i], team) == 0) {
            return 1;
        }
    }
    return 0;
}

// Generate possible picks
void generate_possible_picks() {
    for (int i = 0; i < total_games; i++) {
        if (is_already_picked(games[i].team1) == 0 && games[i].spread < 0) {
            Pick p = {games[i].week, games[i].spread, ""};
            strcpy(p.team, games[i].team1);
            possible_picks[total_possible_picks++] = p;
        } else if (is_already_picked(games[i].team2) == 0 && games[i].spread > 0) {
            Pick p = {games[i].week, games[i].spread, ""};
            strcpy(p.team, games[i].team2);
            possible_picks[total_possible_picks++] = p;
        }
    }
}

// Evaluate pick set
void evaluate_picks(Pick *pick_set, int len, int *min_spread, int *total_spread) {
    *min_spread = abs(pick_set[0].spread);
    *total_spread = 0;

    for (int i = 0; i < len; i++) {
        int abs_spread = abs(pick_set[i].spread);
        *total_spread += abs_spread;
        if (abs_spread < *min_spread) {
            *min_spread = abs_spread;
        }
    }
}

// Combination logic
void find_best_picks(int start, int depth, Pick *current_set) {
    if (depth == total_remaining_weeks) {
        int min_spread, total_spread;
        evaluate_picks(current_set, depth, &min_spread, &total_spread);

        if (min_spread > best_min_spread || (min_spread == best_min_spread && total_spread > best_total_spread)) {
            best_min_spread = min_spread;
            best_total_spread = total_spread;
            memcpy(best_set, current_set, depth * sizeof(Pick));
        }
        return;
    }

    for (int i = start; i < total_possible_picks; i++) {
        int week_already_in_set = 0;
        int team_already_in_set = 0;

        for (int j = 0; j < depth; j++) {
            if (current_set[j].week == possible_picks[i].week) {
                week_already_in_set = 1;
            }
            if (strcmp(current_set[j].team, possible_picks[i].team) == 0) {
                team_already_in_set = 1;
            }
        }

        if (!week_already_in_set && !team_already_in_set) {
            current_set[depth] = possible_picks[i];
            find_best_picks(i + 1, depth + 1, current_set);
        }
    }
}

int main() {
    FILE *file = fopen("games.csv", "r");
    if (!file) {
        printf("Error opening file.\n");
        return 1;
    }

    char line[256];
    fgets(line, sizeof(line), file);  // Skip header line
    while (fgets(line, sizeof(line), file)) {
        sscanf(line, "%d,%3s,%3s,%d", &games[total_games].week, games[total_games].team1, games[total_games].team2, &games[total_games].spread);
        total_games++;
    }
    fclose(file);

    // Calculate remaining weeks
    for (int i = 1; i <= 17; i++) {
        int picked = 0;
        for (int j = 0; j < total_weeks_picked; j++) {
            if (weeks_picked[j] == i) {
                picked = 1;
                break;
            }
        }
        if (!picked) {
            remaining_weeks[total_remaining_weeks++] = i;
        }
    }

    generate_possible_picks();

    Pick current_set[MAX_WEEKS];
    find_best_picks(0, 0, current_set);

    if (best_min_spread > 0) {
        for (int i = 0; i < total_remaining_weeks; i++) {
            printf("Week %d | %s   spread - %d\n", best_set[i].week, best_set[i].team, abs(best_set[i].spread));
            weeks_picked[total_weeks_picked++] = best_set[i].week;
            strcpy(already_picked[total_already_picked++], best_set[i].team);
        }
    } else {
        printf("No valid pick set found.\n");
    }

    // Calculate and print total time
    clock_t end_time = clock();
    double total_seconds = ((double)end_time) / CLOCKS_PER_SEC;

    int hours = (int)(total_seconds / 3600);
    int minutes = (int)((total_seconds - (hours * 3600)) / 60);
    double seconds = total_seconds - (hours * 3600) - (minutes * 60);

    printf("\nTotal time taken for calculation: %d:%02d:%.2f\n", hours, minutes, seconds);

    return 0;
}
