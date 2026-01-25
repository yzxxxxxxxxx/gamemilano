
export enum NavTab {
  HOME = 'home',
  MEDALS = 'medals',
  SCHEDULE = 'schedule',
  PROFILE = 'profile'
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
