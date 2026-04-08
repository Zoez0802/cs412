// app/(tabs)/login.tsx
// Author: Minjie Zuo , 4/6/2026
// This screen lets the user log in and save the token.

import { useState } from 'react';
import { View, Text, TextInput, Pressable, Keyboard } from 'react-native';
import { styles } from '../../assets/my_styles';

export default function LoginScreen() {
  const BASE_URL = 'https://cs-webapps.bu.edu/minjiez/mini_insta';

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [profileId, setProfileId] = useState(0);
  // this message is used to show the login result to the user, such as success or failure, or any error messages.
  const [message, setMessage] = useState(''); 

  //fixing the login error:302   
  //tips from professor
  // step 1: get login url and expect the csrf token and save it
  //step 2:fetch with the header: csft tokens
  const [csrfToken, setCsrfToken] = useState('');


  // Get the csrftoken value from the cookie header.
  function getCsrf(cText: string | null) {
    if (!cText) return '';

    const parts = cText.split(';');
    for (let i = 0; i < parts.length; i++) {
      const piece = parts[i].trim();
      if (piece.startsWith('csrftoken=')) {
        return piece.substring('csrftoken='.length);
      }
    }

    return '';
  }
  
//When the user presses the Login button，this function sends a POST request to the backend with the entered username and password. It then processes the response to extract the authentication token and profile ID, which are saved in the component's state. The function also handles various error cases, such as non-JSON responses or failed login attempts, and updates the message state accordingly to inform the user of the outcome.
 async function handleLogin() {
    Keyboard.dismiss();//i added this because after pressing the login button, the keyboard will cover the message text, so this will hide the keyboard after pressing the button. This is not related to the login logic, just a UI improvement.
    try {
      // step 1:
      // make a GET request first so Django can send back a csrf cookie
      const csrfRes = await fetch(`${BASE_URL}/login/`, {
        method: 'GET',
        credentials: 'include',
      });

      // try to read csrf token
      const cookieH =csrfRes.headers.get('set-cookie') ||csrfRes.headers.get('Set-Cookie');
      const FCsrfToken = getCsrf(cookieH);

      if (!FCsrfToken) {
        setMessage('Could not get CSRF token.');
        return;
      }

      setCsrfToken(FCsrfToken);

      // step 2:
      // send login request with csrf token in header
      const res = await fetch(`${BASE_URL}/api/login`, {
        method: 'POST',
        credentials: 'include',
        headers: {'Content-Type': 'application/json','Accept': 'application/json','X-CSRFToken': FCsrfToken,},
        body: JSON.stringify({username: username,password: password,}),
      });

      const text = await res.text();
      let data: any = null;

      try {
        data = JSON.parse(text);
      } catch (err) {
        setMessage('Oops, Server did not return JSON.');
        return;
      }

      if (res.ok) {
        setToken(data.token);
        setProfileId(data.profile_id);
        setMessage('Login successful :)');

        // Save the token and profile ID in global variables 
        // fixed token and profileID type error
        (globalThis as any).token = data.token;
        (globalThis as any).profileId = data.profile_id;
      
      } else {
        setMessage(data.error || 'Login failed.');
        
      }
    } catch (error) {
      console.log('Login error:', error);
      setMessage('Something went wrong :( Try again later.');
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>Login</Text>

      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry={true}
      />

      <Pressable style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Login</Text>
      </Pressable>

      {message ? <Text style={styles.smallText}>{message}</Text> : null}
      {token ? <Text style={styles.smallText}>Token: {token}</Text> : null}
      {profileId ? <Text style={styles.smallText}>Profile ID: {profileId}</Text> : null}
    </View>
  );
}