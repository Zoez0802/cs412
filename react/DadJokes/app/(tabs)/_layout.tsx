// app/(tabs)/_layout.tsx
// Author: Minjie Zuo , 3/28/2026
// This file defines the layout for the tab screen in the DadJokes application.

import React from 'react';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import { Tabs } from 'expo-router';

import Colors from '@/constants/Colors';
import { useColorScheme } from '@/components/useColorScheme';
import { useClientOnlyValue } from '@/components/useClientOnlyValue';


// Define the tab layout for the application.
export default function TabLayout() {
  'This is the layout for the tab screen. It defines the three tabs: Home, Jokes, and Add Joke.';
  const colorScheme = useColorScheme();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint,
        headerShown: useClientOnlyValue(false, true),
      }}
    >
    {/* Index screen*/}
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          // display icon for this tab, similar to example
          tabBarIcon: ({ color }) => (
            <FontAwesome name="home" size={24} color={color} />
          ),
        }}
      />

      {/* Jokes list screen */}
      <Tabs.Screen
        name="jokes_list"  
        options={{
          title: 'Jokes',
          // display icon for this tab
          tabBarIcon: ({ color }) => (
            <FontAwesome name="list" size={24} color={color} />
          ),
        }}
      />

      {/* Add joke screen */}
      <Tabs.Screen
        name="add_joke" 
        options={{
          title: 'Add Joke',
          // display icon for this tab
          tabBarIcon: ({ color }) => (
            <FontAwesome name="plus" size={24} color={color} />
          ),
        }}
      />

    </Tabs>
  );
}