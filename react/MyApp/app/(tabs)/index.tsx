// index.tsx
// Author: Minjie Zuo (minjiez@bu.edu), 3/22/2026
// This file defines the index screen for the application.

import { Image } from 'react-native';
import { Text, View } from '@/components/Themed';
import { styles } from '../../assets/my_styles';

/**
 * Display the index screen with a short welcome message.
 */
export default function IndexScreen() {
  return (
    <View style={styles.container}>
      {/* Page title */}
      <Text style={styles.titleText}>Welcome</Text>

      {/* Intro text */}
      <Text style={styles.bodyText}>
        Hi! My name is Zoe. Welcome to my first mobile app. Use the tabs below to explore my interests and learn
        more about this project!!!!
      </Text>

      {/* load from an image file stored in the MyApp/assets/images directory */}
      <Image
        source={require('../../assets/images/me.png')}
        style={styles.image}
      />
    </View>
  );
}