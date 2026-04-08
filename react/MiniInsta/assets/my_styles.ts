// assets/my_styles.ts
// Author: Minjie Zuo , 4/6/2026
// This file defines the styles used across the MiniInsta application. It includes styles for containers, text, images, inputs, and buttons to ensure a consistent look and feel throughout the app.

import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },

  titleText: {
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 14,
  },

  sectionTitle: {
    fontSize: 22,
    fontWeight: '600',
    marginBottom: 10,
    marginTop: 10,
  },

  box: {
    marginBottom: 16,
    padding: 14,
    borderRadius: 12,
    backgroundColor: '#f4f4f4',
  },

  nameText: {
    fontSize: 22,
    fontWeight: '600',
    marginBottom: 4,
  },

  handleText: {
    fontSize: 16,
    marginBottom: 8,
  },

  bioText: {
    fontSize: 15,
    marginBottom: 10,
  },

  infoText: {
    fontSize: 14,
    marginTop: 6,
  },

  postText: {
    fontSize: 16,
    marginBottom: 8,
  },

  image: {
    width: '100%',
    height: 220,
    borderRadius: 10,
    marginTop: 10,
  },

  input: {
    borderWidth: 1,
    borderColor: '#bdbdbd',
    borderRadius: 10,
    padding: 12,
    marginBottom: 12,
    backgroundColor: 'white',
  },

  button: {
    backgroundColor: '#4f46e5',
    padding: 12,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 6,
  },

  buttonText: {
    color: 'white',
    fontWeight: '600',
    fontSize: 16,
  },

  smallText: {
    fontSize: 13,
    marginTop: 8,
  },
});