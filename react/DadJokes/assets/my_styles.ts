// my_styles.ts
// Author: Minjie Zuo (minjiez@bu.edu), 3/29/2026
// This file stores shared styles for the app.

import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 30,
    paddingBottom: 20,
    backgroundColor: '#f7f4ef',
  },

  titleText: {
    fontSize: 30,
    fontWeight: '700',
    textAlign: 'center',
    marginBottom: 20,
    color: '#3b2f2f',
  },

  box: {
    backgroundColor: '#fffaf5',
    borderRadius: 18,
    padding: 18,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#eadfd3',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.08,
    shadowRadius: 6,
  },

  jokeText: {
    fontSize: 18,
    lineHeight: 27,
    color: '#2f2f2f',
    marginBottom: 12,
  },

  infoText: {
    fontSize: 13,
    color: '#7a6f66',
    marginBottom: 12,
  },

  image: {
    width: '100%',
    height: 220,
    borderRadius: 14,
    resizeMode: 'cover',
    marginTop: 6,
  },

  input: {
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#d8cfc4',
    borderRadius: 14,
    fontSize: 16,
    marginBottom: 14,
    color: '#2f2f2f',   
    paddingVertical: 14,
    paddingHorizontal: 16,
  },

  button: {
    backgroundColor: '#6b4f4f',
    paddingVertical: 14,
    borderRadius: 14,
    alignItems: 'center',
    marginTop: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.12,
    shadowRadius: 4,
    elevation: 2,
  },

  buttonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },

  listContent: {
    paddingBottom: 30,
  },
});