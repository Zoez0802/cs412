// detail.tsx
// Author: Minjie Zuo (minjiez@bu.edu), 3/22/2026
// This file defines the detail screen for the application.

import { ScrollView, Image } from 'react-native';
import { Text, View } from '@/components/Themed';
import { styles } from '../../assets/my_styles';

export default function DetailScreen() {
  return (
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      <Text style={styles.titleText}>My Interests</Text>

      {/* Skiing section */}
      <Text style={styles.sectionTitle}>Skiing</Text>
      <Text style={styles.bodyText}>
        Skiing is one of my favorite activities because it is exciting,
        and full of energy. I love the feeling of gliding down the slopes and watching the beautiful mountain scenery.
      </Text>
      <Image
        source={{ uri: 'https://cs-people.bu.edu/minjiez/images/ski.jpg' }}
        style={styles.image}
      />
      <Text style={styles.bodyText}>
      I enjoy the speed and the feeling of being outdoors in the mountains.
      </Text>



      {/* Photography section */}
      <Text style={styles.sectionTitle}>Photography</Text>
      <Text style={styles.bodyText}>
        My another interest is photography because it allows me to capture meaningful
        moments and beautiful scenes. I like using photos to remember places I
        have visited and moments I want to keep.
      </Text>
      <Image
        source={{ uri:'https://cs-people.bu.edu/minjiez/images/me.jpg' }}
        style={styles.image}
      />
      <Text style={styles.bodyText}>
        Photography is a way for me to express myself and share my perspective.
      </Text>



      {/* Travel section */}
      <Text style={styles.sectionTitle}>Travel</Text>
      <Text style={styles.bodyText}>
        Traveling lets me explore new places, experience different cultures, and
        see landscapes that are very different from everyday life. 
      </Text>
      <Image
        source={{ uri: 'https://cs-people.bu.edu/minjiez/images/travel1.jpg' }}
        style={styles.image}
      />

      <Text style={styles.bodyText}>
      So far, I have been to many places in the US and some other countries. I look forward to traveling more in the future and seeing more of the world!
      </Text>
    </ScrollView>
  );
}