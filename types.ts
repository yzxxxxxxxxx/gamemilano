
export enum NavTab {
  HOME = 'home',
  MEDALS = 'medals',
  SCHEDULE = 'schedule',
  HISTORY = 'history'
}


export interface OlympicEdition {
  year: number;
  location: string;
  countries_count?: number;
  events_count?: number;
}

export interface HistoricalMedalEntry {
  rank: number;
  country: string;
  iso: string;
  gold: number;
  silver: number;
  bronze: number;
  total: number;
}

export interface HistoricalEvent {
  id: string;
  sport_name: string;
  event_name: string;
  gold_country?: string;
  gold_iso?: string;
  silver_country?: string;
  silver_iso?: string;
  bronze_country?: string;
  bronze_iso?: string;
}

export interface OlympicEvent {
  id: string;
  sport: string;
  discipline: string;
  title: string;
  time: string;
  location: string;
  isTeamChina: boolean;
  type: 'final' | 'preliminary' | 'medal';
  reminded: boolean;
}

export interface MedalEntry {
  rank: number;
  country: string;
  iso: string;
  gold: number;
  silver: number;
  bronze: number;
}
