// my_styles.ts
// Author: Minjie Zuo (minjiez@bu.edu), 3/22/2026
// This file defines the shared styles for the application.

import { StyleSheet } from 'react-native';

/**
 * Define the style information
 */
export const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },

  scrollContainer: {
    alignItems: 'center',
    padding: 20,
  },

  titleText: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 12,
    textAlign: 'center',
  },

  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
    marginTop: 10,
    textAlign: 'center',
  },

  bodyText: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 24,
  },

  image: {
    width: 180,
    height: 180,
    resizeMode: 'contain',
  },

});