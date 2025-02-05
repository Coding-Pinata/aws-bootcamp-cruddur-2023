import './DesktopNavigation.css';
import {ReactComponent as Logo} from './svg/logo.svg';
import DesktopNavigationLink from '../components/DesktopNavigationLink';
import CrudButton from '../components/CrudButton';
import ProfileInfo from '../components/ProfileInfo';

export default function DesktopNavigation(props) {

  let button;
  let profile;
  let notificationsLink;
  let messagesLink;
  let profileLink;
  if (props.user) {
    button = <CrudButton setPopped={props.setPopped} />;
    profile = <ProfileInfo user={props.user} />;
    notificationsLink = <DesktopNavigationLink 
      url="/notifications" 
      name="Notifications" 
      handle="notifications" 
      active={props.active} />;
    messagesLink = <DesktopNavigationLink 
      url="/messages"
      name="Messages"
      handle="messages" 
      active={props.active} />
    profileLink = <DesktopNavigationLink 
      url="/@Mariachi in a Jar" 
      name="Profile"
      handle="profile"
      active={props.active} />
  }

  return (
    <nav>
      <Logo className='logo' />
      <DesktopNavigationLink 
        url="/" 
        name="Home"
        handle="home"
        active={props.active} />
      {/* <DesktopNavigationLink 
        url="/notifications" 
        name="Notifications"
        handle="notifications"
        active={props.active} />
      <DesktopNavigationLink 
        url="/messages" 
        name="Messages"
        handle="messages"
        active={props.active} />
      <DesktopNavigationLink 
        url="/profile" 
        name="Profile"
        handle="profile"
        active={props.active} /> */}

      {/* In comparison to the above approach, 
      coding this way makes sure that the following three pages are
      not shown to a not-logged-in user  */}
      {notificationsLink}  
      {messagesLink}
      {profileLink}
      <DesktopNavigationLink 
        url="/more" 
        name="More" 
        handle="more"
        active={props.active} />
      {button}
      {profile}
    </nav>
  );
}