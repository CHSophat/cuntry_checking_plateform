<template>
  <div class="default-layout">
    <header class="header">
      <nav class="navbar">
        <div class="logo">Check country names using AI</div>
        <ul class="nav-links">
          <li><RouterLink to="/">Home</RouterLink></li>
          <li><RouterLink to="/about">About</RouterLink></li>
        </ul>
      </nav>

      <!-- Country Generator Section -->
      <div class="search-section">
        <div class="search-container">
          <h2>🌍 Discover Countries & Generate AI Information</h2>
          <p class="section-description">Search for any country and generate detailed AI-powered information about it.</p>
          <div class="search-input-group">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by country name, capital, or ISO code (e.g., Vietnam, Hanoi, VN)..."
              class="search-input"
              @input="handleSearch"
              aria-label="Search for country"
            />
            <button class="search-btn" @click="performSearch" aria-label="Search">
              🔍 Search
            </button>
          </div>

          <!-- Show Search Results First -->
          <div v-if="searchAttempted && searchResults.length > 0 && !selectedCountry" class="results-container">
            <div class="results-header">
              <h3>📌 Search Results: {{ searchResults.length }} Country(ies) Found</h3>
              <p class="results-subtitle">Click on a country to generate AI-powered information</p>
            </div>
            
            <!-- Results List - Simple Preview -->
            <div class="simple-results-list">
              <div
                v-for="country in searchResults"
                :key="country.id"
                class="country-preview"
                @click="selectCountry(country)"
                :class="{ 'active': selectedCountry?.id === country.id }"
              >
                <div class="preview-header">
                  <h5>{{ country.name }}</h5>
                  <span class="iso-badge-small">{{ country.iso_code }}</span>
                </div>
                <p class="preview-info">Capital: <strong>{{ country.capital }}</strong></p>
                <button class="generate-btn" @click.stop="selectCountry(country)">
                  ✨ Generate AI Info
                </button>
              </div>
            </div>
          </div>

          <!-- No Results Message -->
          <div v-if="searchAttempted && searchResults.length === 0" class="no-results">
            <p>
              No countries found matching "{{ searchQuery }}". Try a different country name to generate content.
            </p>
          </div>
        </div>
      </div>
    </header>

    <!-- AI Modal Overlay -->
    <div v-if="selectedCountry" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <!-- Loading Alert -->
        <div v-if="isGenerating" class="generating-alert-modal">
          <div class="alert-content">
            <div class="loading-spinner"></div>
            <h3>✨ Generating AI Information...</h3>
            <p>Analyzing and synthesizing comprehensive information about {{ selectedCountry.name }}</p>
            <div class="dots-animation">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>

        <!-- AI Content (shown after generation) -->
        <div v-show="!isGenerating" class="modal-ai-content fade-in">
          <div class="modal-header">
            <h2>🤖 AI-Generated Information about {{ selectedCountry.name }}</h2>
            <button class="modal-close-btn" @click="closeModal" :disabled="isGenerating">✕</button>
          </div>

          <div class="country-card ai-card">
            <!-- Country Header -->
            <div class="country-header">
              <h4>{{ selectedCountry.name }}</h4>
              <span class="iso-badge">{{ selectedCountry.iso_code }}</span>
            </div>

            <!-- Basic Information -->
            <div class="info-section">
              <h5>📍 Basic Information</h5>
              <div class="info-grid">
                <div class="info-item">
                  <span class="label">Capital:</span>
                  <span class="value">{{ selectedCountry.capital }}</span>
                </div>
                <div class="info-item">
                  <span class="label">Coordinates:</span>
                  <span class="value">{{ selectedCountry.latitude }}°, {{ selectedCountry.longitude }}°</span>
                </div>
              </div>
            </div>

            <!-- Details Section (AI Generated) -->
            <div class="info-section">
              <h5>📋 Country Details</h5>
              <p class="ai-text">
                {{ generateCountryDetails(selectedCountry) }}
              </p>
            </div>

            <!-- Tourism Section (AI Generated) -->
            <div class="info-section">
              <h5>✈️ Tourism & Attractions</h5>
              <p class="ai-text">
                {{ generateTourismInfo(selectedCountry) }}
              </p>
            </div>

            <!-- Culture Section (AI Generated) -->
            <div class="info-section">
              <h5>🎭 Culture & Heritage</h5>
              <p class="ai-text">
                {{ generateCultureInfo(selectedCountry) }}
              </p>
            </div>

            <!-- People Section (AI Generated) -->
            <div class="info-section">
              <h5>👥 People & Society</h5>
              <p class="ai-text">
                {{ generatePeopleInfo(selectedCountry) }}
              </p>
            </div>

            <!-- Major Tourism Sites -->
            <div class="info-section" v-if="selectedCountry?.tourism?.major_sites && selectedCountry.tourism.major_sites.length > 0">
              <h5>🏛️ Major Tourism Sites</h5>
              <div class="major-sites-list">
                <div class="site-info" v-for="(site, index) in selectedCountry.tourism.major_sites" :key="index" @click="toggleSiteDetails(index)" :class="{ 'expanded': expandedSiteIndex === index }">
                  <div class="site-header">
                    <span class="site-number">{{ index + 1 }}</span>
                    <span class="site-name">{{ site }}</span>
                    <span class="expand-icon">{{ expandedSiteIndex === index ? '▼' : '▶' }}</span>
                  </div>
                  <div v-if="expandedSiteIndex === index" class="site-description">
                    <p>{{ generateSiteDescription(selectedCountry.name, site, index) }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Quick Facts -->
            <div class="quick-facts">
              <span class="fact-badge">🌍 Diverse Culture</span>
              <span class="fact-badge">📚 Rich History</span>
              <span class="fact-badge">🏆 Unique Traditions</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <main class="main-content">
      <slot></slot>
    </main>

    <footer class="footer">
      <p>&copy; 2026 Country Information Search. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';

const searchQuery = ref('');
const searchResults = ref([]);
const searchAttempted = ref(false);
const allCountries = ref([]);
const generationCounter = ref(0);
const selectedCountry = ref(null);
const isGenerating = ref(false);
const expandedSiteIndex = ref(null);

// Load countries from API
onMounted(async () => {
  try {
    const response = await fetch('http://localhost:3000/countries');
    allCountries.value = await response.json();
  } catch (error) {
    console.error('Error loading countries:', error);
  }
});

// Handle input change with debounce
const handleSearch = () => {
  clearTimeout(window.searchTimeout);
  window.searchTimeout = setTimeout(() => {
    if (searchQuery.value.length > 0) {
      performSearch();
    } else {
      searchResults.value = [];
      searchAttempted.value = false;
    }
  }, 300);
};

// Perform search and filter countries
const performSearch = () => {
  const query = searchQuery.value.toLowerCase().trim();
  if (query.length === 0) {
    searchResults.value = [];
    searchAttempted.value = false;
    selectedCountry.value = null;
    return;
  }

  searchResults.value = allCountries.value.filter((country) => {
    const name = country.name.toLowerCase();
    const capital = country.capital.toLowerCase();
    const isoCode = country.iso_code.toLowerCase();
    
    return (
      name.includes(query) || 
      capital.includes(query) || 
      isoCode.includes(query)
    );
  });

  searchAttempted.value = true;
  selectedCountry.value = null;
  generationCounter.value = 0;
};

// Select a country to generate AI info with loading animation
const selectCountry = async (country) => {
  selectedCountry.value = country;
  isGenerating.value = true;
  generationCounter.value = 0;
  
  // Simulate AI generation delay (like ChatGPT typing)
  await new Promise(resolve => setTimeout(resolve, 1200));
  
  isGenerating.value = false;
};

// Close modal function
const closeModal = () => {
  if (!isGenerating.value) {
    selectedCountry.value = null;
    expandedSiteIndex.value = null;
  }
};

// Toggle site details expansion
const toggleSiteDetails = (index) => {
  expandedSiteIndex.value = expandedSiteIndex.value === index ? null : index;
};

// Generate AI description for major sites
const generateSiteDescription = (countryName, siteName, siteIndex) => {
  const siteDescriptions = {
    "Vietnam": {
      0: "Ha Long Bay is a stunning UNESCO World Heritage Site featuring dramatic limestone karsts rising from emerald waters. This natural wonder spans over 1,600 square kilometers and is famous for its picturesque landscape, vibrant marine ecosystem, and traditional junk boat experiences. Visitors can enjoy cave exploration, kayaking, and island hopping in this iconic destination.",
      1: "Hanoi, the capital of Vietnam, is a vibrant city blending ancient traditions with modern development. The city features the iconic Hoan Kiem Lake, the charming Old Quarter with narrow streets, and significant historical landmarks including the Ho Chi Minh Mausoleum and Temple of Literature.",
      2: "Ho Chi Minh City, formerly Saigon, is Vietnam's largest and most dynamic metropolis. The city showcases French colonial architecture, bustling markets, war history museums, and a thriving food scene. The Reunification Palace and Ben Thanh Market are must-visit attractions.",
      3: "Hoi An is a perfectly preserved ancient town on Vietnam's coast, featuring well-maintained Chinese and Japanese influenced architecture from the 15th-19th centuries. The lantern-lit streets, traditional tailor shops, and beautiful riverside setting make it one of Southeast Asia's most charming destinations.",
      4: "Sapa is a mountainous town in northwest Vietnam known for its stunning terraced rice fields, misty peaks, and vibrant hill tribe cultures. Located at 1,600 meters altitude, Sapa offers trekking opportunities, local markets, and breathtaking natural landscapes."
    },
    "Egypt": {
      0: "The Great Pyramids of Giza are among the world's most iconic structures, standing as testaments to ancient Egyptian engineering. Built around 4,500 years ago, these monumental tombs showcase incredible precision and continue to captivate millions of visitors annually.",
      1: "The Great Sphinx, with its lion's body and human head, is a colossal statue carved from limestone bedrock. This mysterious monument has guarded the pyramids for millennia and remains an enigmatic symbol of ancient Egypt's grandeur and mystery.",
      2: "The Luxor Temples are magnificent structures built during the reign of Amenhotep III and later modified by various pharaohs. These temples showcase exquisite carvings, towering columns, and reliefs depicting religious ceremonies and royal triumphs.",
      3: "Aswan is a picturesque city on the Nile River's banks, famous for its golden-hued sand dunes and tranquil atmosphere. Visitors can enjoy felucca sailing, temple visits, and access to the impressive Aswan High Dam and Abu Simbel temples.",
      4: "The Valley of the Kings is a royal burial site containing the tombs of numerous pharaohs including Tutankhamun. Hidden in the desert hills, these ancient tombs are adorned with intricate hieroglyphic paintings and artifacts revealing the wealth and beliefs of ancient rulers."
    },
    "France": {
      0: "The Eiffel Tower is the most recognizable monument in the world, standing 330 meters tall on the Champ de Mars. Built in 1889, this iron lattice structure offers breathtaking views of Paris and has become the ultimate symbol of romance and French culture.",
      1: "The Louvre Museum houses the world's largest art museum, featuring over 38,000 works including the Mona Lisa and Venus de Milo. This former royal palace showcases masterpieces spanning from ancient civilizations to the 19th century.",
      2: "The Palace of Versailles is a magnificent royal residence featuring opulent rooms, stunning gardens, and elaborate fountains. This UNESCO World Heritage Site represents the absolute power of French monarchy and is one of Europe's grandest palaces.",
      3: "Mont-Saint-Michel is a breathtaking medieval abbey perched atop a rocky tidal island connected by a narrow causeway. The dramatic architecture and strategic location have made this Normandy landmark one of France's most visited destinations.",
      4: "Provence's lavender fields create stunning purple landscapes, especially during summer bloom season. This picturesque region is renowned for its fragrant lavender crops, charming villages, local wine production, and Mediterranean charm."
    }
  };

  // Get country-specific descriptions or use generic description
  if (siteDescriptions[countryName] && siteDescriptions[countryName][siteIndex]) {
    return siteDescriptions[countryName][siteIndex];
  }

  // Generic AI-style descriptions based on site index
  const genericDescriptions = [
    `${siteName} is one of the most renowned tourist destinations in ${countryName}. This site attracts visitors from around the world who come to experience its unique characteristics, historical significance, and cultural importance. The location offers unforgettable experiences that reflect the essence of ${countryName}'s heritage.`,
    `${siteName} stands as a testament to ${countryName}'s rich cultural and historical legacy. Visitors to this destination discover remarkable architecture, natural beauty, and authentic cultural experiences. Its popularity among tourists demonstrates the enduring appeal of this iconic location.`,
    `Travelers visiting ${siteName} experience the true essence of ${countryName}'s tourism offerings. The site combines natural splendor with historical significance, creating a destination that appeals to diverse interests. Expert guides and modern facilities enhance the visitor experience.`,
    `${siteName} represents ${countryName}'s commitment to preserving its cultural treasures while welcoming international visitors. The site features impressive displays of local traditions, craftsmanship, and natural wonders that captivate tourists year-round.`,
    `As one of ${countryName}'s premier attractions, ${siteName} showcases the country's diverse attractions and world-class tourism infrastructure. Visitors consistently praise the site's beauty, accessibility, and the warm hospitality of local communities.`
  ];

  return genericDescriptions[siteIndex % genericDescriptions.length];
};

// AI-Generated Content Functions with variations
const generateCountryDetails = (country) => {
  const detailsOptions = {
    Afghanistan: [
      `${country.name} is located in South Asia and Central Asia, serving as a crucial bridge between regions. With a strategic geographic position, it covers vast mountainous terrain with diverse ecosystems. The country has a rich historical significance, being part of the ancient Silk Road.`,
      `${country.name} stands at the crossroads of Asia, featuring dramatic mountain ranges and historic valleys. The terrain shapes the lives of its diverse population, from high plateaus to river valleys. This geographic diversity creates unique cultural and economic zones throughout the nation.`,
      `${country.name}'s landscape encompasses the Hindu Kush mountains and fertile plains. Located at coordinates ${country.latitude}°, ${country.longitude}°, it has always held strategic importance in regional politics and trade. The capital, ${country.capital}, serves as the nation's political and cultural center.`,
    ],
    Albania: [
      `${country.name} is a Balkan nation with a Mediterranean coastline, featuring stunning natural landscapes combining mountains, beaches, and historical sites. The country has made significant progress in recent decades, transitioning to a democratic market economy.`,
      `${country.name} blends Mediterranean charm with Balkan character, offering diverse geography from Adriatic shores to mountain peaks. The nation's position has made it a cultural crossroads throughout history, influencing its unique identity and traditions.`,
      `${country.name} lies in Southeast Europe with strategic access to the Adriatic Sea. From ${country.capital}, the capital, to remote mountain villages, the country preserves both modern development and ancient heritage.`,
    ],
    Vietnam: [
      `${country.name} is a Southeast Asian country known for its S-shaped geography stretching along the coast. It has transformed into one of Asia's dynamic economies through rapid industrialization and modernization. The country boasts a 3,000-year history with profound cultural influences.`,
      `${country.name}'s distinctive coastline and river deltas make it geographically unique in Southeast Asia. The rapid economic transformation has created a vibrant blend of traditional villages and modern cities, each offering distinct cultural experiences.`,
      `${country.name} extends from the mountains of the north to the Mekong Delta in the south, featuring diverse ecosystems and cultures. Located at ${country.latitude}°, ${country.longitude}°, the country continues to evolve as a major regional power.`,
    ],
  };

  const options = detailsOptions[country.name] || [
    `${country.name} is a fascinating country with unique geographical and cultural characteristics. Located at coordinates ${country.latitude}°, ${country.longitude}°, the capital is ${country.capital}. The nation has contributed significantly to world history.`,
    `${country.name} offers diverse landscapes and rich cultural heritage. With ${country.capital} as its capital, the nation continues to play an important role in regional and global affairs.`,
  ];

  return options[(generationCounter.value + country.id) % options.length];
};

const generateTourismInfo = (country) => {
  const tourismOptions = {
    Afghanistan: [
      `Tourism in ${country.name} is gradually opening to adventurous travelers. Notable attractions include the Band-e Amir National Park with its stunning turquoise lakes, and historical sites in Herat and Kandahar. The Bamiyan Valley remains historically significant.`,
      `${country.name} offers unique tourism experiences for those seeking authentic cultural encounters. The high mountain regions provide breathtaking scenery, while ancient cities tell stories of the Silk Road. Adventure seekers can explore pristine wilderness areas.`,
      `Travelers to ${country.name} can discover hidden gems including mountain trekking routes, historic bazaars, and archaeological sites. The country's tourism is developing, offering immersive experiences in one of Asia's most culturally rich nations.`,
    ],
    Albania: [
      `${country.name} offers diverse tourism experiences with the Riviera featuring pristine beaches, and the Albanian Alps providing stunning mountain scenery. UNESCO World Heritage Sites include Berat and Gjirokastër with their well-preserved Ottoman architecture.`,
      `The tourism landscape of ${country.name} includes beautiful Adriatic beaches, mountain hiking trails, and charming ancient towns. The country is increasingly popular with adventure tourists and those seeking authentic Balkan experiences.`,
      `${country.name} attracts visitors seeking unspoiled Mediterranean beaches and historic mountain villages. Lake Ohrid offers both natural beauty and water activities, while archaeological sites reveal the country's ancient past.`,
    ],
    Vietnam: [
      `${country.name} is a top Southeast Asian tourism destination. Ha Long Bay, a UNESCO World Heritage Site, features stunning limestone karsts and emerald waters. Ho Chi Minh City and Hanoi offer vibrant urban experiences with rich history.`,
      `Tourism in ${country.name} encompasses natural wonders and cultural treasures. From bustling street markets to tranquil countryside, visitors experience authentic Southeast Asian culture. The country's diverse attractions appeal to all types of travelers.`,
      `${country.name}'s tourism scene combines historical significance with natural beauty. Mountain regions, river experiences, and coastal areas each offer distinct adventures. The country's welcoming people enhance every visitor's experience.`,
    ],
  };

  const options = tourismOptions[country.name] || [
    `${country.name} offers diverse tourism opportunities for all types of travelers. Visitors can explore historical landmarks, enjoy local cuisine, and experience authentic cultural practices.`,
  ];

  return options[(generationCounter.value + country.id * 2) % options.length];
};

const generateCultureInfo = (country) => {
  const cultureOptions = {
    Afghanistan: [
      `${country.name}'s culture is deeply rooted in Islamic traditions combined with Persian, Turkic, and indigenous Pashtun influences. Traditional music, poetry, and literature play vital roles in cultural expression. Afghan carpets are world-renowned for their intricate designs.`,
      `Culture in ${country.name} reflects centuries of diverse influences creating a unique tapestry of traditions. Music, dance, and poetry remain central to social life. The nation's artistic heritage includes renowned textile craftsmanship.`,
      `${country.name}'s cultural practices emphasize hospitality, honor, and community values. Traditional crafts, including carpet weaving and metalwork, are still practiced and celebrated. The culture continues to thrive despite historical challenges.`,
    ],
    Albania: [
      `${country.name} blends Balkan, Byzantine, and Ottoman cultural influences. The traditional folk music and dances are vibrant expressions of national identity. Literature and poetry have deep historical roots dating back centuries.`,
      `Cultural life in ${country.name} combines Mediterranean warmth with Balkan tradition. National festivals celebrate folk customs, music, and dance. The country preserves ancient traditions while embracing modern cultural expressions.`,
      `${country.name}'s heritage includes diverse artistic expressions from ancient Illyrian times to modern era. Traditional crafts, music, and cuisine reflect the nation's multicultural influences and rich history.`,
    ],
    Vietnam: [
      `${country.name}'s culture is shaped by thousands of years of history with strong Confucian, Buddhist, and indigenous influences. Traditional arts include water puppetry, lacquerware, and silk painting. Vietnamese literature and poetry are celebrated worldwide.`,
      `Cultural traditions in ${country.name} blend spiritual beliefs with practical life wisdom. Martial arts, traditional medicine, and agricultural practices reflect deep cultural knowledge. Family values remain central to society.`,
      `${country.name}'s artistic heritage includes acclaimed traditional crafts, performing arts, and literary traditions. Modern Vietnamese culture celebrates both ancestral practices and contemporary creativity.`,
    ],
  };

  const options = cultureOptions[country.name] || [
    `${country.name} has a rich cultural heritage shaped by centuries of history. Traditional arts, crafts, music, and literature remain important expressions of national identity.`,
  ];

  return options[(generationCounter.value + country.id * 3) % options.length];
};

const generatePeopleInfo = (country) => {
  const peopleOptions = {
    Afghanistan: [
      `The people of ${country.name} are known for their resilience, hospitality, and strong sense of community. The population is ethnically diverse, including Pashtuns, Tajiks, Uzbeks, and Hazaras. Family and tribal bonds are fundamental to social structure.`,
      `${country.name}'s people exemplify strength through adversity and deep cultural pride. Community values and family loyalty are paramount. The population's linguistic diversity reflects the nation's complex history and geography.`,
      `People in ${country.name} maintain strong traditions of hospitality and honor. The population's resilience shapes daily life and cultural practices. Diverse ethnic communities contribute to the nation's rich cultural mosaic.`,
    ],
    Albania: [
      `Albanians are known for their warm hospitality and strong family values. The population shares a common language and cultural heritage dating back to ancient Illyrian times. Albanians take pride in their independent spirit and cultural identity.`,
      `${country.name}'s people are characterized by their welcoming nature and strong social bonds. The population maintains deep connections to traditional values while embracing modern opportunities. Community celebration and family gatherings are central to life.`,
      `The people of ${country.name} possess a unique cultural identity rooted in ancient history. Contemporary Albanian society balances respect for traditions with progressive values and aspirations.`,
    ],
    Vietnam: [
      `Vietnamese people are industrious, entrepreneurial, and deeply connected to their heritage. The culture emphasizes respect for elders, family unity, and social harmony. Vietnamese are known for their culinary traditions, creating some of Asia's most beloved cuisines.`,
      `${country.name}'s population embodies adaptability and determination. People maintain strong family networks and community ties. The younger generation combines traditional values with modern global perspectives.`,
      `The people of ${country.name} demonstrate remarkable entrepreneurial spirit and creative energy. Family-centered values coexist with individual aspiration. Vietnamese people have contributed significantly to regional and global innovation.`,
    ],
  };

  const options = peopleOptions[country.name] || [
    `The people of ${country.name} are characterized by their unique cultural identity and values. Strong family bonds and community ties form the foundation of society.`,
  ];

  return options[(generationCounter.value + country.id * 4) % options.length];
};
</script>

<style scoped>
.default-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  width: 100%;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  font-size: 24px;
  font-weight: bold;
  letter-spacing: 0.5px;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  transition: color 0.3s ease, border-bottom 0.3s ease;
  padding: 0.5rem 0;
}

.nav-links a:hover {
  color: #ffd700;
  border-bottom: 2px solid #ffd700;
}

.nav-links a.router-link-active {
  color: #ffd700;
  border-bottom: 2px solid #ffd700;
}

/* Search Section Styles */
.search-section {
  background: rgba(0, 0, 0, 0.1);
  padding: 2rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.search-container h2 {
  font-size: 28px;
  margin-bottom: 0.5rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.section-description {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.search-input-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-family: inherit;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.search-input:focus {
  outline: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.search-btn {
  padding: 12px 24px;
  background-color: #ffd700;
  color: #333;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.search-btn:hover {
  background-color: #ffed4e;
  transform: translateY(-2px);
}

.search-btn:active {
  transform: translateY(0);
}

/* Results Container */
.results-container {
  margin-top: 2rem;
}

.results-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(255, 215, 0, 0.3);
}

.results-header h3 {
  font-size: 20px;
  color: #ffd700;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  margin: 0 0 0.5rem 0;
}

.results-subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  margin: 0;
}

/* Simple Results List */
.simple-results-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.country-preview {
  background: white;
  border-radius: 8px;
  padding: 1.25rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.country-preview:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.country-preview.active {
  border-color: #667eea;
  background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.preview-header h5 {
  margin: 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.iso-badge-small {
  background-color: #667eea;
  color: white;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: bold;
  letter-spacing: 0.5px;
}

.preview-info {
  color: #666;
  font-size: 14px;
  margin: 0 0 0.75rem 0;
}

.generate-btn {
  width: 100%;
  padding: 8px 12px;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.generate-btn:hover {
  background-color: #764ba2;
  transform: translateY(-2px);
}

/* AI Content Section */
.ai-content-section {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  margin-top: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.ai-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #667eea;
}

.ai-header h2 {
  margin: 0;
  color: #667eea;
  font-size: 24px;
}

.close-ai-btn {
  padding: 8px 16px;
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-ai-btn:hover:not(:disabled) {
  background-color: #e0e0e0;
  border-color: #999;
}

.close-ai-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Loading/Generating Alert */
.generating-alert {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  background: linear-gradient(135deg, #f0f4ff 0%, #f8f9ff 100%);
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  border: 2px solid #667eea;
}

.alert-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e0e0e0;
  border-top: 4px solid #667eea;
  border-right: 4px solid #764ba2;
  border-radius: 50%;
  animation: spinLoader 1s linear infinite;
}

@keyframes spinLoader {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.alert-content h3 {
  margin: 0;
  color: #667eea;
  font-size: 20px;
}

.alert-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.dots-animation {
  display: flex;
  gap: 6px;
  justify-content: center;
  margin-top: 0.5rem;
}

.dots-animation span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #667eea;
  animation: dotsBounce 1.4s infinite;
}

.dots-animation span:nth-child(2) {
  animation-delay: 0.2s;
}

.dots-animation span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dotsBounce {
  0%, 80%, 100% {
    opacity: 0.5;
    transform: translateY(0);
  }
  40% {
    opacity: 1;
    transform: translateY(-10px);
  }
}

/* Fade-in animation for content */
.fade-in {
  animation: fadeInContent 0.6s ease-in;
}

@keyframes fadeInContent {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Modal Overlay Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
  overflow-y: auto;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.4s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.generating-alert-modal {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  background: linear-gradient(135deg, #f0f4ff 0%, #f8f9ff 100%);
  padding: 2rem;
  border-bottom: 2px solid #667eea;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  border-bottom: 2px solid #667eea;
  background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 100%);
  position: sticky;
  top: 0;
  z-index: 100;
}

.modal-header h2 {
  margin: 0;
  color: #667eea;
  font-size: 26px;
}

.modal-close-btn {
  width: 40px;
  height: 40px;
  padding: 0;
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 50%;
  font-size: 20px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.modal-close-btn:hover:not(:disabled) {
  background-color: #e0e0e0;
  border-color: #999;
}

.modal-close-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.modal-ai-content {
  padding: 2rem;
}

.results-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.country-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.country-card.ai-card {
  border-left: 4px solid #667eea;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
}

.country-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.country-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #667eea;
}

.country-header h4 {
  color: #667eea;
  font-size: 24px;
  margin: 0;
}

.iso-badge {
  background-color: #667eea;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  letter-spacing: 0.5px;
}

.info-section {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: rgba(102, 126, 234, 0.05);
  border-radius: 6px;
  border-left: 3px solid #667eea;
}

.info-section h5 {
  color: #667eea;
  font-size: 16px;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item .label {
  font-weight: 600;
  color: #333;
  font-size: 13px;
  margin-bottom: 0.25rem;
}

.info-item .value {
  color: #666;
  font-size: 14px;
}

.ai-text {
  color: #555;
  line-height: 1.7;
  font-size: 14px;
  margin: 0;
  text-align: justify;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Major Sites List */
.major-sites-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.site-info {
  background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
  border: 1px solid #667eea;
  border-radius: 6px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.site-info:hover {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
  border-color: #764ba2;
}

.site-info.expanded {
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.25);
}

.site-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  transition: background-color 0.3s ease;
}

.site-info:hover .site-header {
  background-color: rgba(102, 126, 234, 0.05);
}

.site-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  font-weight: bold;
  font-size: 13px;
  flex-shrink: 0;
}

.site-name {
  color: #333;
  font-size: 14px;
  font-weight: 600;
  flex: 1;
}

.expand-icon {
  color: #667eea;
  font-size: 12px;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.site-info.expanded .expand-icon {
  transform: rotate(0deg);
}

.site-description {
  padding: 0 1rem 1rem 1rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.site-description p {
  margin: 0;
  color: #555;
  font-size: 13px;
  line-height: 1.6;
  text-align: justify;
}

.quick-facts {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.fact-badge {
  background-color: #e8eef7;
  color: #667eea;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.fact-badge:hover {
  background-color: #667eea;
  color: white;
}

/* No Results Message */
.no-results {
  background: rgba(255, 255, 255, 0.1);
  border-left: 4px solid #ffd700;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.no-results p {
  color: #fff;
  font-size: 16px;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
}

.footer {
  background-color: #333;
  text-align: center;
  padding: 2rem;
  border-top: 1px solid #555;
  margin-top: 2rem;
}

.footer p {
  margin: 0;
  color: #999;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-links {
    gap: 1rem;
  }

  .search-input-group {
    flex-direction: column;
  }

  .results-list {
    grid-template-columns: 1fr;
  }

  .logo {
    font-size: 20px;
  }

  .search-container h2 {
    font-size: 24px;
  }
}
</style>
