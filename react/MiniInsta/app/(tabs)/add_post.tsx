// app/(tabs)/add_post.tsx
// Author: Minjie Zuo, 4/6/2026
// This screen allows users to create a new post by entering a caption and an image URL. It sends a POST request to the backend to create the post and displays a success or error message based on the response. The styles are imported from the shared styles file to maintain a consistent look across the app.

import { useState } from 'react';
import { View, Text, TextInput, Pressable, Keyboard} from 'react-native';
import { styles } from '../../assets/my_styles';

export default function AddPostScreen() {
  const BASE_URL = 'https://cs-webapps.bu.edu/minjiez/mini_insta';

  // store user input
  const [caption, setCaption] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [message, setMessage] = useState('');

  // send one new post to the API
  async function handlePost() {
    Keyboard.dismiss(); // hide keyboard after pressing the button, this is just a UI improvement, not related to the post logic
    const token = (globalThis as any).token;
    const profileId = (globalThis as any).profileId;

    if (!token || !profileId) {
      setMessage('Please login first.');
      return;
    }

    const newP = {
      profile: profileId,
      caption: caption,
      image_url: imageUrl,
      token: token,
    };

    try {
      const res = await fetch(`${BASE_URL}/api/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },body: JSON.stringify(newP),
      });

      const text = await res.text();
      console.log('post status:', res.status);


      if (!res.ok) {
        setMessage('Failed to create post :(');
        return;
      }

      setMessage('Post created!');
      setCaption('');
      setImageUrl('');
    } catch (error) {
      console.log('Post error:', error);
      setMessage('Something went wrong :(');
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>Create Post</Text>

      <TextInput
        style={styles.input}
        placeholder="Write a caption"
        value={caption}
        onChangeText={setCaption}
      />

      <TextInput
        style={styles.input}
        placeholder="Paste image URL"
        value={imageUrl}
        onChangeText={setImageUrl}
      />

      <Pressable style={styles.button} onPress={handlePost}>
        <Text style={styles.buttonText}>Post</Text>
      </Pressable>

      {message ? <Text style={styles.smallText}>{message}</Text> : null}
    </View>
  );
}