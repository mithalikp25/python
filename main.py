// =============================
// Weather-Based Outfit Recommender in C
// =============================
// Description:
// This interactive console program allows users to input weather details (temperature and condition)
// and receive customized outfit recommendations based on the weather. It simulates behavior similar
// to a basic AI stylist by suggesting outfit types, accessories, and shoes.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

// =============================
// CONSTANTS AND DEFINITIONS
// =============================

#define MAX_LEN 100
#define NUM_OUTFITS 3
#define NUM_ITEMS 3
#define NUM_ACCESSORIES 5
#define NUM_SHOES 5
#define MAX_CITIES 5

// Temperature validation constants
#define MIN_TEMP -50.0
#define MAX_TEMP 50.0

// ANSI color codes for colorful terminal output
#define GREEN   "\033[1;32m"
#define BLUE    "\033[1;34m"
#define CYAN    "\033[1;36m"
#define RED     "\033[1;31m"
#define YELLOW  "\033[1;33m"
#define MAGENTA "\033[1;35m"
#define BOLD    "\033[1m"
#define RESET   "\033[0m"

// =============================
// STRUCTURE DEFINITIONS
// =============================

// Outfit structure to hold a title and an array of clothing items
typedef struct {
    char title[MAX_LEN];
    char items[NUM_ITEMS][MAX_LEN];
} Outfit;

// Weather structure to hold city name, temperature, and condition
typedef struct {
    char city[MAX_LEN];
    float temp;
    char condition[MAX_LEN];
} Weather;

// =============================
// GLOBAL DATA ARRAYS
// =============================

// Outfit options for cold weather
Outfit cold_outfits[NUM_OUTFITS] = {
    {"Winter Warrior", {"Thick Trench Coat", "Corduroy Pants", "Wool Turtleneck"}},
    {"Arctic Explorer", {"Insulated Puffer Jacket", "Thermal Leggings", "Merino Wool Sweater"}},
    {"Cozy Professional", {"Wool Overcoat", "Dark Jeans", "Cashmere Sweater"}}
};

// Outfit options for moderate weather
Outfit moderate_outfits[NUM_OUTFITS] = {
    {"Smart Casual", {"Cotton Long Sleeve", "Chinos", "Light Cardigan"}},
    {"Weekend Relaxed", {"Henley Shirt", "Khaki Pants", "Zip-up Hoodie"}},
    {"Urban Explorer", {"Denim Jacket", "Joggers", "Graphic Tee"}}
};

// Outfit options for hot weather
Outfit hot_outfits[NUM_OUTFITS] = {
    {"Summer Cool", {"Linen Button-up", "Cotton Shorts", "Baseball Cap"}},
    {"Beach Ready", {"Tank Top", "Board Shorts", "Sun Hat"}},
    {"City Heat", {"Moisture-wicking Tee", "Linen Pants", "Cooling Towel"}}
};

// Accessory suggestions
char cold_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Wool Scarf", "Insulated Gloves", "Warm Beanie", "Fleece Headband", "Thermal Socks"
};

char moderate_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Baseball Cap", "Stylish Watch", "Leather Belt", "Sunglasses", "Light Scarf"
};

char hot_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Wide-Brim Hat", "Cooling Bandana", "UV Protection Wristband", "Portable Fan", "Sweat Towel"
};

// Shoe suggestions
char cold_shoes[NUM_SHOES][MAX_LEN] = {
    "Waterproof Boots", "Insulated Sneakers", "Warm Chelsea Boots", "Snow Boots", "Thermal Loafers"
};

char moderate_shoes[NUM_SHOES][MAX_LEN] = {
    "Comfortable Sneakers", "Canvas Shoes", "Casual Loafers", "Walking Boots", "Slip-on Shoes"
};

char hot_shoes[NUM_SHOES][MAX_LEN] = {
    "Breathable Sandals", "Flip-Flops", "Mesh Sneakers", "Water Shoes", "Ventilated Slip-ons"
};

// Weather memory for convenience
Weather last_weather = {"", 0.0, ""};
int has_last_weather = 0;

// =============================
// FUNCTION DECLARATIONS
// =============================

void print_banner();
void strip_newline(char *str);
int get_valid_choice(int max);
void simulate_loading(const char *msg);
void display_outfits(Outfit outfits[], int size);
void display_options(char options[][MAX_LEN], int count);
const char* get_category(float temp);
void get_weather_input(Weather *weather);
void recommend_outfit(const Weather *weather);
void wait_for_user();
void print_divider();
void repeat_menu();
void farewell();
void display_weather_info(const Weather *weather);
void show_weather_tips(const Weather *weather);
void clear_input_buffer();

// =============================
// UTILITY FUNCTIONS
// =============================

// Print program banner with formatting
void print_banner() {
    printf(GREEN);
    printf("\n==========================================\n");
    printf("   🌤️  Weather-Based Outfit Recommender  👕\n");
    printf("==========================================\n" RESET);
    printf(CYAN "Your personal AI stylist for any weather!\n" RESET);
    printf(YELLOW "✨ Get personalized outfit suggestions based on current conditions\n" RESET);
}

// Remove newline character from string
void strip_newline(char *str) {
    size_t len = strlen(str);
    if (len > 0 && str[len - 1] == '\n') {
        str[len - 1] = '\0';
    }
}

// Clear input buffer to handle scanf issues
void clear_input_buffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

// Get a valid user menu choice within range
int get_valid_choice(int max) {
    int choice;
    char input[10];
    
    while (1) {
        printf(YELLOW "Enter your choice (1-%d): " RESET, max);
        
        if (fgets(input, sizeof(input), stdin) != NULL) {
            if (sscanf(input, "%d", &choice) == 1 && choice >= 1 && choice <= max) {
                return choice;
            }
        }
        
        printf(RED "❌ Invalid input. Please enter a number between 1 and %d.\n" RESET, max);
    }
}

// Simulate loading animation with message
void simulate_loading(const char *msg) {
    printf(CYAN "🔄 %s", msg);
    fflush(stdout);
    
    for (int i = 0; i < 4; i++) {
        printf(".");
        fflush(stdout);
        // Cross-platform delay
        for (volatile long j = 0; j < 50000000; j++);
    }
    printf(" Done!" RESET "\n");
}

// Display outfit titles and their items
void display_outfits(Outfit outfits[], int size) {
    for (int i = 0; i < size; i++) {
        printf(BLUE "%d. " BOLD "%s" RESET "\n", i + 1, outfits[i].title);
        for (int j = 0; j < NUM_ITEMS; j++) {
            printf("   • %s\n", outfits[i].items[j]);
        }
        printf("\n");
    }
}

// Display options such as accessories or shoes
void display_options(char options[][MAX_LEN], int count) {
    for (int i = 0; i < count; i++) {
        printf("%d. %s\n", i + 1, options[i]);
    }
}

// Determine weather category based on temperature
const char* get_category(float temp) {
    if (temp < 10.0) return "cold";
    else if (temp <= 25.0) return "moderate";
    else return "hot";
}

// Display current weather information with enhanced formatting
void display_weather_info(const Weather *weather) {
    printf(MAGENTA "\n🌡️  Weather Summary for " BOLD "%s" RESET MAGENTA ":\n" RESET, weather->city);
    printf("Temperature: " BOLD "%.1f°C" RESET "\n", weather->temp);
    printf("Condition: " BOLD "%s" RESET "\n", weather->condition);
    
    const char *category = get_category(weather->temp);
    if (strcmp(category, "cold") == 0) {
        printf("Category: ❄️  " CYAN BOLD "Cold Weather" RESET "\n");
    } else if (strcmp(category, "moderate") == 0) {
        printf("Category: 🌤️  " YELLOW BOLD "Moderate Weather" RESET "\n");
    } else {
        printf("Category: ☀️  " RED BOLD "Hot Weather" RESET "\n");
    }
}

// Show weather-specific tips and advice
void show_weather_tips(const Weather *weather) {
    const char *category = get_category(weather->temp);
    
    printf(CYAN "\n💡 Weather Tips:\n" RESET);
    
    if (strcmp(category, "cold") == 0) {
        printf("• Layer up to trap warm air between clothing\n");
        printf("• Don't forget to cover extremities (hands, feet, head)\n");
        printf("• Choose moisture-wicking base layers\n");
    } else if (strcmp(category, "moderate") == 0) {
        printf("• Perfect weather for versatile layering\n");
        printf("• Consider bringing a light jacket for temperature changes\n");
        printf("• Comfortable walking weather - great for outdoor activities\n");
    } else {
        printf("• Stay hydrated and seek shade when possible\n");
        printf("• Choose light-colored, loose-fitting clothes\n");
        printf("• Don't forget sun protection (hat, sunscreen)\n");
    }
}

// Take user input for weather details with improved validation
void get_weather_input(Weather *weather) {
    printf("\n📍 Enter your city: ");
    if (has_last_weather) {
        printf("(or press Enter for '%s') ", last_weather.city);
    }
    
    if (fgets(weather->city, MAX_LEN, stdin) == NULL) {
        printf(RED "Error reading city name.\n" RESET);
        exit(1);
    }
    strip_newline(weather->city);
    
    // If user just pressed enter, use last city
    if (strlen(weather->city) == 0 && has_last_weather) {
        strcpy(weather->city, last_weather.city);
        printf("✅ Using previous city: " BOLD "%s" RESET "\n", weather->city);
    }
    
    // Validate city name is not empty
    if (strlen(weather->city) == 0) {
        strcpy(weather->city, "Unknown City");
        printf("🏙️  Using default: %s\n", weather->city);
    }

    // Temperature input with validation
    while (1) {
        printf("🌡️  Enter temperature (°C): ");
        if (has_last_weather) {
            printf("(or press Enter for %.1f°C) ", last_weather.temp);
        }
        
        char temp_input[20];
        if (fgets(temp_input, sizeof(temp_input), stdin) != NULL) {
            strip_newline(temp_input);
            
            // Check if user wants to use last temperature
            if (strlen(temp_input) == 0 && has_last_weather) {
                weather->temp = last_weather.temp;
                printf("✅ Using previous temperature: " BOLD "%.1f°C" RESET "\n", weather->temp);
                break;
            }
            
            if (sscanf(temp_input, "%f", &weather->temp) == 1) {
                if (weather->temp >= MIN_TEMP && weather->temp <= MAX_TEMP) {
                    break;
                } else {
                    printf(RED "❌ Temperature must be between %.1f and %.1f°C.\n" RESET, MIN_TEMP, MAX_TEMP);
                }
            } else {
                printf(RED "❌ Please enter a valid number.\n" RESET);
            }
        }
    }

    printf("🌦️  Enter weather condition (e.g., Sunny, Rainy, Cloudy): ");
    if (fgets(weather->condition, MAX_LEN, stdin) == NULL) {
        printf(RED "Error reading weather condition.\n" RESET);
        exit(1);
    }
    strip_newline(weather->condition);
    
    // Default condition if empty
    if (strlen(weather->condition) == 0) {
        strcpy(weather->condition, "Clear");
        printf("☀️  Using default condition: %s\n", weather->condition);
    }

    // Save current weather as last used
    strcpy(last_weather.city, weather->city);
    last_weather.temp = weather->temp;
    strcpy(last_weather.condition, weather->condition);
    has_last_weather = 1;
}

// Recommend outfit based on weather input with enhanced features
void recommend_outfit(const Weather *weather) {
    display_weather_info(weather);
    show_weather_tips(weather);
    
    const char *category = get_category(weather->temp);
    Outfit *chosen_outfit;
    char (*acc)[MAX_LEN];
    char (*shoe)[MAX_LEN];

    // Case-insensitive weather condition check
    char condition_lower[MAX_LEN];
    strcpy(condition_lower, weather->condition);
    for (int i = 0; condition_lower[i]; i++) {
        condition_lower[i] = tolower(condition_lower[i]);
    }

    // Enhanced weather-specific advice
    printf(YELLOW "\n🌦️  Special Weather Considerations:\n" RESET);
    if (strstr(condition_lower, "rain") || strstr(condition_lower, "drizzle")) {
        printf(BLUE "☔ Rain detected! Recommendations:\n");
        printf("   • Bring an umbrella or waterproof jacket\n");
        printf("   • Choose water-resistant footwear\n");
        printf("   • Avoid light-colored clothing\n" RESET);
    } else if (strstr(condition_lower, "snow")) {
        printf(CYAN "❄️ Snowy conditions! Recommendations:\n");
        printf("   • Extra layers and waterproof outer shell\n");
        printf("   • Non-slip, insulated footwear\n");
        printf("   • Hand and foot warmers\n" RESET);
    } else if (strstr(condition_lower, "wind")) {
        printf(YELLOW "💨 Windy weather! Recommendations:\n");
        printf("   • Windbreaker or fitted jacket\n");
        printf("   • Secure accessories (hats, scarves)\n");
        printf("   • Avoid loose, flowing garments\n" RESET);
    } else if (strstr(condition_lower, "sun") || strstr(condition_lower, "clear")) {
        printf(YELLOW "☀️ Sunny conditions! Recommendations:\n");
        printf("   • UV protection is essential\n");
        printf("   • Light colors reflect heat\n");
        printf("   • Stay hydrated\n" RESET);
    } else {
        printf("🌤️  General weather - perfect for versatile styling!\n");
    }

    printf("\n👔 Choose your outfit style:\n");
    if (strcmp(category, "cold") == 0) {
        display_outfits(cold_outfits, NUM_OUTFITS);
        chosen_outfit = &cold_outfits[get_valid_choice(NUM_OUTFITS) - 1];
        acc = cold_accessories;
        shoe = cold_shoes;
    } else if (strcmp(category, "moderate") == 0) {
        display_outfits(moderate_outfits, NUM_OUTFITS);
        chosen_outfit = &moderate_outfits[get_valid_choice(NUM_OUTFITS) - 1];
        acc = moderate_accessories;
        shoe = moderate_shoes;
    } else {
        display_outfits(hot_outfits, NUM_OUTFITS);
        chosen_outfit = &hot_outfits[get_valid_choice(NUM_OUTFITS) - 1];
        acc = hot_accessories;
        shoe = hot_shoes;
    }

    printf("\n🎒 Choose your accessory:\n");
    display_options(acc, NUM_ACCESSORIES);
    int acc_choice = get_valid_choice(NUM_ACCESSORIES) - 1;

    printf("\n👟 Choose your footwear:\n");
    display_options(shoe, NUM_SHOES);
    int shoe_choice = get_valid_choice(NUM_SHOES) - 1;

    // Enhanced final outfit display
    printf(GREEN "\n✨ Your Perfect Outfit Recommendation:\n" RESET);
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf(BLUE "Style: " BOLD "%s" RESET "\n", chosen_outfit->title);
    printf("Clothing Items:\n");
    for (int i = 0; i < NUM_ITEMS; i++) {
        printf("  • " BOLD "%s" RESET "\n", chosen_outfit->items[i]);
    }
    printf("Accessory: " BOLD "%s" RESET "\n", acc[acc_choice]);
    printf("Footwear: " BOLD "%s" RESET "\n", shoe[shoe_choice]);
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf(GREEN "Have a stylish and comfortable day! 😎✨\n" RESET);
}

// Print a divider between sections
void print_divider() {
    printf("\n" CYAN "═══════════════════════════════════════════\n" RESET);
}

// Ask user whether to repeat with improved formatting
void repeat_menu() {
    printf(YELLOW "\n🔄 Would you like to get another outfit recommendation?\n" RESET);
    printf("1. " GREEN "Yes, try another city/weather" RESET "\n");
    printf("2. " RED "No, exit program" RESET "\n");
}

// Print enhanced exit message
void farewell() {
    printf(GREEN "\n🎉 Thank you for using the Weather-Based Outfit Recommender!\n");
    printf("Stay stylish and weather-ready! ✨👗👔🌟\n");
    printf("Remember: Confidence is the best accessory! 💫\n" RESET);
}

// =============================
// MAIN FUNCTION
// =============================

int main() {
    printf(CYAN "Initializing Weather-Based Outfit Recommender...\n" RESET);
    
    while (1) {
        Weather current_weather = {"", 0.0, ""}; // Initialize struct
        print_banner();
        get_weather_input(&current_weather);
        simulate_loading("Analyzing weather and finding perfect outfits");
        recommend_outfit(&current_weather);
        print_divider();
        repeat_menu();
        int choice = get_valid_choice(2);
        if (choice == 2) break;
        
        // Clear screen effect
        printf("\n\n");
    }
    
    farewell();
    return 0;
}