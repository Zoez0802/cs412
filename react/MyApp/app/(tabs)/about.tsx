// about.tsx
// Author: Minjie Zuo (minjiez@bu.edu), 3/22/2026
// This file defines the about screen for the application.

import { Image } from 'react-native';
import { Text, View } from '@/components/Themed';
import { styles } from '../../assets/my_styles';

export default function AboutScreen() {
  return (
    <View style={styles.container}>
      {/* Page title */}
      <Text style={styles.titleText}>About This App</Text>

      {/* About text */}
      <Text style={styles.bodyText}>
        This app is a simple React Native project built with Expo. It uses tab
        navigation to organize multiple screens and displays text and images to
        introduce my interests. The detail page is scrollable so users can view
        more content in one place.
      </Text>

      {/* Local app image */}
      <Image
        source={require('../../assets/images/favicon.png')} style={styles.image}
        />
    </View>
  );
}