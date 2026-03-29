// add_joke.tsx
// Author: Minjie Zuo (minjiez@bu.edu), 3/29/2026
// This screen lets the user add a new joke to the API.

import { useState } from 'react';
import { TextInput, Pressable } from 'react-native';
import { Text, View } from '@/components/Themed';
import { styles } from '../../assets/my_styles';

export default function AddJokeScreen() {
  // store user input
  const [name, setName] = useState('');
  const [jokeText, setJokeText] = useState('');

  // send one joke to the API
  async function addJoke() {
    'This function sends a POST request to the Django API to add a new joke with the user input'
    const newJoke = {
      text: jokeText,
      contributor: name,
    };

    //debugging statements 
    console.log('About to send POST request');
    console.log(newJoke);

    //send a POST request to the Django API to create a new joke
    const res = await fetch(
      'https://cs-webapps.bu.edu/minjiez/dadjokes/api/jokes',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',// sending JSON data
        },
        body: JSON.stringify(newJoke),//convert the joke object into JSON format
      }
    );

    //debugging statements to check response
    console.log('Response status:', res.status);
    const data = await res.json();
    console.log('Response data:', data);

    setJokeText('');
    setName('');
  }

  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>Add Joke</Text>

    <TextInput
      style={styles.input}
      placeholder="Enter a joke"
      placeholderTextColor="#9a8f85" // lighter color for placeholder
      value={jokeText}
      onChangeText={setJokeText}// update jokeText state when user types
    />

    <TextInput
      style={styles.input}
      placeholder="Contributor name"
      placeholderTextColor="#9a8f85"
      value={name}
      onChangeText={setName}
    />
      <Pressable style={styles.button} onPress={addJoke}>
        <Text style={styles.buttonText}>Submit</Text>
      </Pressable>
    </View>
  );
}