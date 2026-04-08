// app/(tabs)/_layout.tsx
// Author: Minjie Zuo
// This file defines the layout for the tab screen in the MiniInsta application. It sets up the three tabs: My Profile, Feed, and Add Post, each with its own icon.

import { Tabs } from 'expo-router';
import FontAwesome from '@expo/vector-icons/FontAwesome';

// Define the tab layout for the application.
export default function TabLayout() {
  return (
    
    <Tabs>
      <Tabs.Screen
        name="index"
        options={{
          title: 'My Profile',
          tabBarIcon: ({ color }) => (
            <FontAwesome name="user" size={22} color={color} />
          ),
        }}
      />


      <Tabs.Screen
        name="feed"
        options={{
          title: 'Feed',
          tabBarIcon: ({ color }) => (
            <FontAwesome name="home" size={22} color={color} />
          ),
        }}
      />

      <Tabs.Screen
        name="add_post"
        options={{
          title: 'Add Post',
          tabBarIcon: ({ color }) => (
            <FontAwesome name="plus" size={22} color={color} />
          ),
        }}
      /> 
      
      <Tabs.Screen
        name="login"
        options={{
          title: 'Login',
          tabBarIcon: ({ color }) => (
            <FontAwesome name="sign-in" size={22} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}