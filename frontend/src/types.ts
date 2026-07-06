export type MinutesData = {
  title?: string;
  date?: string;
  attendees?: string[];
  summary?: string[];
  decisions?: string[];
  action_items?: { task?: string; owner?: string; deadline?: string }[];
};

export type EmailItem = {
  from: string;
  subject: string;
  category: 'Urgent' | 'Action Needed' | 'FYI';
  one_line_summary: string;
  suggested_reply: string | null;
};

export type Preview = { name: string; file_id: string };
